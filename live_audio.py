#!/usr/bin/env python3
"""
Live Audio Recording Script

Records 5 seconds of audio from the default microphone using PyAudio
and saves it as output.wav with proper error handling.
"""

import pyaudio
import wave
import sys
import time
from pathlib import Path

# Audio recording parameters
CHUNK = 1024          # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit)
CHANNELS = 1          # Mono audio
RATE = 44100          # Sample rate (Hz)
RECORD_SECONDS = 5    # Duration of recording
OUTPUT_FILENAME = "output.wav"

def record_audio():
    """
    Record audio from the default microphone and save to WAV file.
    
    Returns:
        bool: True if recording was successful, False otherwise
    """
    audio = None
    stream = None
    
    try:
        # Initialize PyAudio
        audio = pyaudio.PyAudio()
        
        # Check if microphone is available
        try:
            # Get default input device info
            default_device = audio.get_default_input_device_info()
            print(f"Using microphone: {default_device['name']}")
        except OSError as e:
            print(f"Error: No microphone found or microphone access denied: {e}")
            return False
        
        # Open audio stream
        try:
            stream = audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
        except OSError as e:
            print(f"Error: Could not open audio stream: {e}")
            print("Please check if your microphone is connected and not being used by another application.")
            return False
        
        print(f"🎤 Recording started... ({RECORD_SECONDS} seconds)")
        print("Speak now!")
        
        # Record audio data
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                
                # Show progress indicator
                progress = (i + 1) / (RATE / CHUNK * RECORD_SECONDS)
                dots = "." * int(progress * 10)
                print(f"\rRecording: [{dots:<10}] {progress*100:.0f}%", end="", flush=True)
                
            except OSError as e:
                print(f"\nError during recording: {e}")
                return False
        
        print(f"\n✅ Recording finished!")
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        
        # Save the recorded data as WAV file
        try:
            output_path = Path(OUTPUT_FILENAME)
            with wave.open(str(output_path), 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
            
            print(f"💾 Audio saved as: {output_path.absolute()}")
            
            # Display file info
            file_size = output_path.stat().st_size
            print(f"📊 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            
            return True
            
        except Exception as e:
            print(f"Error saving audio file: {e}")
            return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    finally:
        # Clean up resources
        if stream:
            try:
                stream.stop_stream()
                stream.close()
            except:
                pass
        
        if audio:
            try:
                audio.terminate()
            except:
                pass

def check_dependencies():
    """
    Check if required dependencies are available.
    
    Returns:
        bool: True if all dependencies are available, False otherwise
    """
    try:
        import pyaudio
        import wave
        return True
    except ImportError as e:
        print(f"Error: Missing required dependency: {e}")
        print("Please install PyAudio using: pip install pyaudio")
        return False

def main():
    """Main function to run the audio recording script."""
    print("🎵 Live Audio Recording Script")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if output file already exists
    output_path = Path(OUTPUT_FILENAME)
    if output_path.exists():
        response = input(f"⚠️  {OUTPUT_FILENAME} already exists. Overwrite? (y/n): ")
        if response.lower() not in ['y', 'yes']:
            print("Recording cancelled.")
            sys.exit(0)
    
    # Record audio
    success = record_audio()
    
    if success:
        print("🎉 Recording completed successfully!")
        
        # Ask if user wants to play the recorded audio (optional)
        try:
            import subprocess
            import platform
            
            play_response = input("🔊 Would you like to play the recorded audio? (y/n): ")
            if play_response.lower() in ['y', 'yes']:
                system = platform.system().lower()
                if system == "windows":
                    subprocess.run(["start", OUTPUT_FILENAME], shell=True, check=True)
                elif system == "darwin":  # macOS
                    subprocess.run(["open", OUTPUT_FILENAME], check=True)
                elif system == "linux":
                    subprocess.run(["xdg-open", OUTPUT_FILENAME], check=True)
                else:
                    print("Automatic playback not supported on this system.")
        except Exception as e:
            print(f"Could not play audio: {e}")
    
    else:
        print("❌ Recording failed. Please check your microphone setup.")
        sys.exit(1)

if __name__ == "__main__":
    main()