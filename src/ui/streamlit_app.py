#!/usr/bin/env python3
"""
AI Public Speaking Coach - Streamlit App

A Streamlit application for analyzing public speaking performance
with live and recorded feedback modes.
"""

import streamlit as st
from pathlib import Path

from datetime import datetime
import time

def main():
    """Main Streamlit application."""
    
    # Page configuration
    try:
        st.set_page_config(
        page_title="AI Public Speaking Coach",
        page_icon="🎤",
        layout="wide",
        initial_sidebar_state="expanded"
        )
    except:
        print("Page already configured")
    
    # Main title
    st.title("🎤 AI Public Speaking Coach")
    st.markdown("---")
    st.markdown("Improve your public speaking skills with AI-powered feedback and analysis!")
    
    # Mode selection with radio buttons
    st.subheader("📋 Select Feedback Mode")
    mode = st.radio(
        "Choose how you'd like to receive feedback:",
        options=["Live Feedback", "Recorded Feedback"],
        index=0,
        help="Live Feedback analyzes your speech in real-time, while Recorded Feedback analyzes uploaded audio/video files."
    )
    
    st.markdown("---")
    
    # Handle different modes
    if mode == "Live Feedback":
        show_live_feedback_mode()
    elif mode == "Recorded Feedback":
        show_recorded_feedback_mode()

def show_live_feedback_mode():
    """Display the Live Feedback mode interface."""
    st.subheader("🔴 Live Feedback Mode")
    
    # Create columns for better layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Placeholder message with styling
        st.info("🚧 Live mode coming soon…")
        
        # Add some additional context
        st.markdown("""
        **Coming Features:**
        - Real-time speech analysis
        - Live gesture detection
        - Instant feedback display
        - Voice clarity monitoring
        """)
        
        # Add a progress indicator to show development status
        st.markdown("**Development Progress:**")
        progress_bar = st.progress(0.3)
        st.caption("30% Complete - Audio processing infrastructure in development")

def show_recorded_feedback_mode():
    """Display the Recorded Feedback mode interface."""
    st.subheader("📁 Recorded Feedback Mode")
    
    # Add option to analyze saved recordings
    st.markdown("### 📂 Analyze Saved Recordings")
    
    # Get project root directory
    try:
        project_root = Path(__file__).parent.parent if Path(__file__).parent.parent.name != "src" else Path(__file__).parent.parent.parent
        video_path = project_root / "data" / "raw" / "video"
        audio_path = project_root / "data" / "raw" / "audio"
    except:
        # Fallback to current directory structure
        project_root = Path.cwd()
        video_path = project_root / "data" / "raw" / "video"
        audio_path = project_root / "data" / "raw" / "audio"
    
    # Collect all saved files
    saved_files = []
    if video_path.exists():
        saved_files.extend(list(video_path.glob("*.mp4")))
    if audio_path.exists():
        saved_files.extend(list(audio_path.glob("*.wav")))
    
    if saved_files:
        saved_file_names = [f.name for f in saved_files]
        selected_saved_file = st.selectbox(
            "Select a saved recording to analyze:",
            ["None"] + saved_file_names
        )
        
        if selected_saved_file != "None":
            # Find the full path
            selected_file_path = None
            for file_path in saved_files:
                if file_path.name == selected_saved_file:
                    selected_file_path = file_path
                    break
            
            if selected_file_path:
                st.success(f"Selected: {selected_saved_file}")
                
                if st.button("🚀 Analyze Saved Recording", type="primary"):
                    with st.spinner("Analyzing your saved recording..."):
                        time.sleep(2)  # Simulate processing
                        st.success("🎉 Analysis complete!")
                        show_mock_analysis_results(selected_saved_file, selected_file_path.suffix)
            
            st.markdown("---")
    else:
        st.info("No saved recordings found. Record some sessions first in Live Feedback mode!")
    
    # Original file upload functionality
    st.markdown("### 📤 Upload New Recording")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload your audio or video file for analysis:",
        type=['wav', 'mp4'],
        help="Supported formats: WAV (audio) and MP4 (video)",
        accept_multiple_files=False
    )
    
    # Handle file upload
    if uploaded_file is not None:
        # Display file information
        st.success("✅ File uploaded successfully!")
        
        # Create columns for file information display
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📄 File Information:**")
            st.write(f"**Name:** {uploaded_file.name}")
            st.write(f"**Type:** {uploaded_file.type}")
            st.write(f"**Size:** {uploaded_file.size:,} bytes ({uploaded_file.size/1024:.1f} KB)")
        
        with col2:
            # Determine file category
            file_extension = Path(uploaded_file.name).suffix.lower()
            if file_extension == '.wav':
                file_category = "🎵 Audio File"
                analysis_type = "Audio analysis will include speech pace, volume, clarity, and filler word detection."
            elif file_extension == '.mp4':
                file_category = "🎬 Video File" 
                analysis_type = "Video analysis will include speech analysis plus gesture recognition and body language assessment."
            else:
                file_category = "📎 Unknown File Type"
                analysis_type = "File type not recognized for analysis."
            
            st.markdown(f"**📊 File Category:** {file_category}")
            st.markdown(f"**🔍 Analysis Type:** {analysis_type}")
        
        # Save uploaded file to /data/raw
        if st.button("💾 Save to Analysis Directory"):
            save_uploaded_file(uploaded_file)
        
        # Print file information to console (as requested)
        print(f"Uploaded file - Name: {uploaded_file.name}, Type: {uploaded_file.type}")
        
        # Show analysis options
        st.markdown("---")
        st.subheader("⚙️ Analysis Options")
        
        # Analysis settings in columns
        analysis_col1, analysis_col2 = st.columns(2)
        
        with analysis_col1:
            analyze_speech = st.checkbox("🗣️ Speech Analysis", value=True)
            if file_extension == '.mp4':
                analyze_gestures = st.checkbox("👋 Gesture Analysis", value=True)
            
        with analysis_col2:
            analyze_pace = st.checkbox("⏱️ Pace & Timing", value=True)
            analyze_emotions = st.checkbox("😊 Emotion Detection", value=False)
        
        # Analysis button
        if st.button("🚀 Start Analysis", type="primary"):
            with st.spinner("Analyzing your file..."):
                # Placeholder for actual analysis
                time.sleep(2)  # Simulate processing time
                
                st.success("🎉 Analysis complete!")
                st.info("🔧 Full analysis features coming soon. File processing infrastructure is ready!")
                
                # Show mock results
                show_mock_analysis_results(uploaded_file.name, file_extension)
    
    else:
        # Show instructions when no file is uploaded
        st.markdown("""
        **📋 Instructions:**
        1. **Analyze saved recordings** from the dropdown above, OR
        2. **Upload new files** using the file uploader below
        3. Configure analysis options
        4. Click "Start Analysis" to begin
        
        **💡 Tips:**
        - Live recordings are automatically saved to `/data/raw`
        - For best results, use clear audio recordings
        - Video files enable additional gesture analysis
        - Files up to 200MB are supported
        """)

def save_uploaded_file(uploaded_file):
    """Save uploaded file to project's data/raw directory."""
    try:
        # Get project root directory
        try:
            project_root = Path(__file__).parent.parent if Path(__file__).parent.parent.name != "src" else Path(__file__).parent.parent.parent
        except:
            project_root = Path.cwd()
        
        # Determine if it's audio or video and set appropriate path
        file_extension = Path(uploaded_file.name).suffix.lower()
        if file_extension in ['.wav', '.mp3', '.m4a']:
            save_path = project_root / "data" / "raw" / "audio"
        elif file_extension in ['.mp4', '.avi', '.mov']:
            save_path = project_root / "data" / "raw" / "video"
        else:
            save_path = project_root / "data" / "raw"
        
        save_path.mkdir(parents=True, exist_ok=True)
        
        # Create filename with timestamp to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"uploaded_{timestamp}_{uploaded_file.name}"
        
        filepath = save_path / filename
        
        # Save the file
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())  # Changed from getvalue() to getbuffer()
        
        st.success(f"✅ File saved to: {filepath.relative_to(project_root)}")
        return str(filepath)
        
    except Exception as e:
        st.error(f"❌ Error saving file: {str(e)}")
        return None

def show_mock_analysis_results(filename: str, file_extension: str):
    """Display mock analysis results."""
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    
    # Create tabs for different analysis types
    if file_extension == '.wav':
        tab1, tab2 = st.tabs(["🎵 Audio Analysis", "📈 Metrics"])
    else:
        tab1, tab2, tab3 = st.tabs(["🎵 Audio Analysis", "🎬 Video Analysis", "📈 Overall Metrics"])
    
    with tab1:
        st.markdown("**Speech Analysis Results:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Speaking Rate", "145 WPM", "5 WPM")
        with col2:
            st.metric("Filler Words", "8", "-2")
        with col3:
            st.metric("Clarity Score", "8.2/10", "0.5")
    
    with tab2:
        if file_extension == '.mp4':
            st.markdown("**Gesture & Body Language:**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Hand Gestures", "Active", "")
                st.metric("Eye Contact", "Good", "+15%")
            with col2:
                st.metric("Posture Score", "7.8/10", "0.3")
                st.metric("Movement", "Natural", "")
        else:
            st.markdown("**Performance Metrics:**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Overall Score", "8.1/10", "0.4")
            with col2:
                st.metric("Confidence Level", "High", "+2 levels")
    
    if file_extension == '.mp4':
        with tab3:
            st.markdown("**Combined Analysis:**")
            st.progress(0.81)
            st.caption("Overall Performance: 8.1/10")


# Sidebar with additional information
def setup_sidebar():
    """Setup the sidebar with app information."""
    st.sidebar.title("ℹ️ About")
    st.sidebar.markdown("""
    **AI Public Speaking Coach** helps you improve your presentation skills through:
    
    - 🎤 Real-time speech analysis
    - 📊 Detailed performance metrics  
    - 👋 Gesture recognition
    - 📈 Progress tracking
    - 💡 Personalized feedback
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📞 Support**")
    st.sidebar.markdown("Having issues? Check our FAQ or contact support.")
    
    if st.sidebar.button("🔄 Reset App"):
        st.rerun()

if __name__ == "__main__":
    st.set_page_config(
        page_title="AI Public Speaking Coach",
        page_icon="🎤",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    setup_sidebar()
    main()