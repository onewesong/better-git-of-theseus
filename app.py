import streamlit as st
import os
import tempfile
import shutil
from git_of_theseus.analyze import analyze
from git_of_theseus.plotly_plots import plotly_stack_plot, plotly_line_plot, plotly_survival_plot

st.set_page_config(page_title="Git of Theseus Dash", layout="wide")

st.title("📊 Git of Theseus - Repository Analysis")

# Sidebar Configuration
st.sidebar.header("Configuration")

repo_path = st.sidebar.text_input("Git Repository Path", value=".")
branch = st.sidebar.text_input("Branch", value="master")

with st.sidebar.expander("Analysis Parameters"):
    cohortfm = st.text_input("Cohort Format", value="%Y")
    interval = st.number_input("Interval (seconds)", value=7 * 24 * 60 * 60)
    procs = st.number_input("Processes", value=2, min_value=1)
    ignore = st.text_area("Ignore (comma separated)").split(",")
    ignore = [i.strip() for i in ignore if i.strip()]

@st.cache_data(show_spinner=False)
def run_analysis(repo_path, branch, cohortfm, interval, procs, ignore):
    return analyze(
        repo_path,
        cohortfm=cohortfm,
        interval=interval,
        ignore=ignore,
        outdir=None,
        branch=branch,
        procs=procs,
        quiet=True
    )

# State management for analysis results
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

if st.sidebar.button("🚀 Run Analysis"):
    with st.spinner("Analyzing repository... this may take a while."):
        try:
            st.session_state.analysis_results = run_analysis(
                repo_path, branch, cohortfm, interval, procs, ignore
            )
            st.success("Analysis completed!")
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.session_state.analysis_results = None

# Main View
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    tab1, tab2, tab3 = st.tabs(["Stack Plot", "Line Plot", "Survival Plot"])

    with tab1:
        st.header("Stack Plot")
        col1, col2 = st.columns([1, 3])
        with col1:
            source_map = {
                "Cohorts": "cohorts",
                "Authors": "authors",
                "Extensions": "exts",
                "Directories": "dirs",
                "Domains": "domains"
            }
            data_source_label = st.selectbox("Data Source", list(source_map.keys()), key="stack_source")
            data_key = source_map[data_source_label]
            normalize = st.checkbox("Normalize to 100%", value=False, key="stack_norm")
            max_n = st.slider("Max Series", 5, 50, 20, key="stack_max_n")
        with col2:
            project_name = os.path.basename(os.path.abspath(repo_path))
            data = results.get(data_key)
            if data:
                fig = plotly_stack_plot(data, normalize=normalize, max_n=max_n, title=project_name)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"Data for {data_source_label} not found.")

    with tab2:
        st.header("Line Plot")
        col1, col2 = st.columns([1, 3])
        with col1:
            data_source_label_line = st.selectbox("Data Source", list(source_map.keys()), key="line_source")
            data_key_line = source_map[data_source_label_line]
            normalize_line = st.checkbox("Normalize to 100%", value=False, key="line_norm")
            max_n_line = st.slider("Max Series", 5, 50, 20, key="line_max_n")
        with col2:
            project_name = os.path.basename(os.path.abspath(repo_path))
            data_line = results.get(data_key_line)
            if data_line:
                fig = plotly_line_plot(data_line, normalize=normalize_line, max_n=max_n_line, title=project_name)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"Data for {data_source_label_line} not found.")

    with tab3:
        st.header("Survival Plot")
        col1, col2 = st.columns([1, 3])
        with col1:
            exp_fit = st.checkbox("Exponential Fit", value=False)
            years = st.slider("Years", 1, 20, 5)
        with col2:
            project_name = os.path.basename(os.path.abspath(repo_path))
            survival_data = results.get("survival")
            if survival_data:
                fig = plotly_survival_plot(survival_data, exp_fit=exp_fit, years=years, title=project_name)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Survival data not found.")

else:
    st.info("👈 Enter a repository path and click 'Run Analysis' to get started.")
