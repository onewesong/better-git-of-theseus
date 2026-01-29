import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import dateutil.parser
import collections
import math
import os
from .utils import generate_n_colors

def _process_stack_line_data(data, max_n=20, normalize=False):
    # Handle dict or file path
    # If it's a file path, load it? But app.py passes dict now. 
    # Let's assume dict for now as per app.py refactor.
    if not isinstance(data, dict):
         # Fallback if needed, though app.py sends dict
        import json
        data = json.load(open(data))

    y = np.array(data["y"])
    labels = data["labels"]
    ts = [dateutil.parser.parse(t) for t in data["ts"]]

    # Sort and filter top N
    if y.shape[0] > max_n:
        # Sort by max value in the series
        js = sorted(range(len(labels)), key=lambda j: max(y[j]), reverse=True)
        
        # Calculate other sum
        other_indices = js[max_n:]
        if other_indices:
            other_sum = np.sum([y[j] for j in other_indices], axis=0)
            
            # Top N indices
            top_js = sorted(js[:max_n], key=lambda j: labels[j])
            
            y = np.array([y[j] for j in top_js] + [other_sum])
            labels = [labels[j] for j in top_js] + ["other"]
        else:
            # Should hopefully not happen if shape[0] > max_n
             pass 
    else:
        # Sort alphabetically for consistency
        js = range(len(labels))
        # strictly speaking existing code didn't sort if <= max_n?
        # "labels = data['labels']" in existing code.
        pass

    y_sums = np.sum(y, axis=0)
    
    # Avoid division by zero
    y_sums[y_sums == 0] = 1.0

    if normalize:
        y = 100.0 * y / y_sums

    return ts, y, labels

def plotly_stack_plot(data, max_n=20, normalize=False, title=None):
    ts, y, labels = _process_stack_line_data(data, max_n, normalize)
    
    fig = go.Figure()
    
    # Use a nice color palette
    colors = px.colors.qualitative.Plotly
    if len(labels) > len(colors):
        colors = px.colors.qualitative.Dark24 # More colors if needed

    for i, label in enumerate(labels):
        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=ts, 
            y=y[i], 
            mode='lines',
            name=label,
            stackgroup='one', # This enables stacking
            line=dict(width=0.5, color=color),
            fillcolor=color # Optional: specific fill color
        ))

    fig.update_layout(
        title=dict(text=title, x=0.5) if title else None,
        yaxis=dict(
            title="Share of lines of code (%)" if normalize else "Lines of code",
            range=[0, 100] if normalize else None
        ),
        xaxis=dict(title="Date"),
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    

    return fig

def plotly_line_plot(data, max_n=20, normalize=False, title=None):
    ts, y, labels = _process_stack_line_data(data, max_n, normalize)

    fig = go.Figure()

    for i, label in enumerate(labels):
         fig.add_trace(go.Scatter(
            x=ts, 
            y=y[i], 
            mode='lines',
            name=label,
            line=dict(width=2)
        ))

    fig.update_layout(
        title=dict(text=title, x=0.5) if title else None,
        yaxis=dict(
            title="Share of lines of code (%)" if normalize else "Lines of code",
            range=[0, 100] if normalize else None
        ),
        xaxis=dict(title="Date"),
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
    )

        
    return fig

def plotly_survival_plot(commit_history, exp_fit=False, years=5, title=None):
    # Logic copied from survival_plot.py
    # commit_history is {sha: [[ts, count], ...]}
    
    deltas = collections.defaultdict(lambda: np.zeros(2))
    total_n = 0
    YEAR = 365.25 * 24 * 60 * 60
    
    # Process history
    # Input might be a list of histories if we support multiple inputs, 
    # but based on app.py we pass a single result["survival"] dict.
    # However, existing survival_plot took a LIST of filenames.
    # Let's support the single dict passed from app.py.
    
    # The logic in survival_plot.py iterates over input_fns, loads them, and computes `all_deltas`.
    # Here we assume `commit_history` IS the content of one such file (the dict).
    
    for commit, history in commit_history.items():
        t0, orig_count = history[0]
        total_n += orig_count
        last_count = orig_count
        for t, count in history[1:]:
            deltas[t - t0] += (count - last_count, 0)
            last_count = count
        deltas[history[-1][0] - t0] += (-last_count, -orig_count)

    # Calculate curve
    P = 1.0
    xs = []
    ys = []
    
    # Sort deltas by time
    sorted_times = sorted(deltas.keys())
    
    total_k = total_n # unused?
    
    for t in sorted_times:
        delta_k, delta_n = deltas[t]
        xs.append(t / YEAR)
        ys.append(100.0 * P)
        
        if total_n > 0:
             P *= 1 + delta_k / total_n
        
        # total_k += delta_k
        total_n += delta_n
        
        if P < 0.05:
            break
            
    fig = go.Figure()
    
    # Main survival curve
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode='lines',
        name='Survival Rate',
        line=dict(color='blue')
    ))

    # Exponential fit
    if exp_fit:
        try:
            import scipy.optimize
            
            # Define loss function for fit
            def fit(k):
                loss = 0.0
                # Re-calculate P stream to fit k
                # Need to iterate again or reuse data?
                # The original code re-iterates.
                
                # Simplified for single dataset:
                curr_total_n = 0
                for _, history in commit_history.items():
                    curr_total_n += history[0][1]
                
                P_fit = 1.0
                curr_total_n_fit = curr_total_n
                
                for t in sorted_times:
                    delta_k, delta_n = deltas[t]
                    pred = curr_total_n_fit * math.exp(-k * t / YEAR)
                    loss += (curr_total_n_fit * P_fit - pred) ** 2
                    if curr_total_n_fit > 0:
                        P_fit *= 1 + delta_k / curr_total_n_fit
                    curr_total_n_fit += delta_n
                return loss

            k_opt = scipy.optimize.fmin(fit, 0.5, maxiter=50, disp=False)[0]
            
            ts_fit = np.linspace(0, years, 100)
            ys_fit = [100.0 * math.exp(-k_opt * t) for t in ts_fit]
            
            half_life = math.log(2) / k_opt
            
            fig.add_trace(go.Scatter(
                x=ts_fit, y=ys_fit,
                mode='lines',
                name=f"Exp. Fit (Half-life: {half_life:.2f} yrs)",
                line=dict(color='red', dash='dash')
            ))
            
        except ImportError:
            pass # Or warn user

    fig.update_layout(
        title=dict(text=title, x=0.5) if title else None,
        yaxis=dict(
            title="lines still present (%)",
            range=[0, 100]
        ),
        xaxis=dict(
            title="Years",
            range=[0, years]
        ),
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
    )


    return fig

def plotly_bar_plot(data, max_n=20, title=None):
    ts, y, labels = _process_stack_line_data(data, max_n, normalize=False)
    
    # Get latest data point (current state)
    latest_values = [row[-1] for row in y]
    
    # Sort by value for better bar chart presentation
    # (Though _process_stack_line_data already does some sorting, we want descending order)
    indices = sorted(range(len(labels)), key=lambda i: latest_values[i], reverse=True)
    
    sorted_labels = [labels[i] for i in indices]
    sorted_values = [latest_values[i] for i in indices]
    
    # Generate colors
    colors = px.colors.qualitative.Plotly
    if len(sorted_labels) > len(colors):
        colors = px.colors.qualitative.Dark24

    fig = go.Figure(go.Bar(
        x=sorted_labels,
        y=sorted_values,
        marker_color=[colors[i % len(colors)] for i in range(len(sorted_labels))]
    ))

    fig.update_layout(
        title=dict(text=f"{title} (Current Distribution)" if title else "Current Distribution", x=0.5),
        yaxis=dict(title="Lines of Code"),
        xaxis=dict(title=""),
        margin=dict(l=20, r=20, t=50, b=100),
    )
    
    return fig
