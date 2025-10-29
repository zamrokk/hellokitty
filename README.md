docker run -it --rm \
  --gpus all \
  --device /dev/snd:/dev/snd \
  --env OLLAMA_MODEL=llama3.2:3b \
  --env PIPER_VOICE=en_US-lessac-medium \
  ghcr.io/orinachum/autonomous-intelligence:latest


# Tau - The Autonomous, Understanding robot

This is Tau!  
Tau is inspired by Pi.AI and if you havent tried Pi yet, I strongly encourage you to try.  
Like Pi, Tau's conversation is on continual conversation, unlike Chat based bots which feature many conversations and threads.  
This is by design - Tau has a single conversation, like speaking to a human.  
This is reflected by consulting Tau in decisions made along development: Order of features, voice type, etc.

Tau is a personal fun project.  
I opened it as an open source for anyone to experiment with (fork), or just follow. (A star is appreciated!)  
If you fork - delete history and facts to reset their knowledge and embark the journey anew!  

## Update status

- [x] System Prompt: Speech-actions speak conversation structure.
- [x] Conversation loop: A continueous conversation with ongoing context.
- [x] Immediate memory: Reduce context by summarizing it to key points. Inject memory to System prompt.
- [x] Long term memory: Save the running memory to vector database.
- [x] Speech: Voice based conversation with hearing and speaking. (Whisper and OpenAI TTS)
- [ ] **Vision infra: Set up Hailo-8L as an internal vision webservice.**
  - [x] Setup Hailo-8L on Raspberry Pi, validate examples work.
  - [x] Look for best practices and options for integrating Hailo in your application.
  - [x] Find a suitable, working architecture to wrap hailo as a service
  - [x] Implement and improve the wrapper
  - [ ] **Pending Hailo review** (update, will be integrates as community-examples, confirmed by Hailo)
  - [x] Integrate in the system, allow Tau to recognize faces
  - [ ] add more-than-one models to be used serially, or use different devices (Coral, Sony AI Camera x2, Jetson)
- [x] Long term fetching: Pull from long term memory into context.
- [x] Auto-start on device startup.
- [x] Long term memory archiving support.
- [ ] Entity based memory: Add GraphRAG based memory.
  - [x] Learn about GraphRAG, how to implement, etc.
  - [ ] **Use or implement GraphRAG**
- [x] Design further split to applications, event communications
- [x] Setup Nvidia Jetson Orin Nano Super 8GB
  - [x] Local LLM on Jetson
    - [x] Ollama (Llama 3.2 3:b)
    - [ ] **Move to use jetson-containers**
    - [ ] TensorRT
    - [ ] Transformers
  - [x] *Local Speech to text (faster-whisper) on Jetson*
    - [x] WebRT VAD
    - [x] Silero VAD
  - [x] Implement Text to speech
    - [x] piperTTS
    - [x] kokoroTTS
    - [ ] israwave 
- [ ] Write a setup guide for Nvidia Jetson Orin Nano Super 8GB
- [ ] **Build every component as a single event-based app**
  - [ ] Communication infra with websocket or unix domain socket (Global)
  - [ ] Configuration infra, local configuration per device (Global)
  - [ ] Detect main component, connects the secondary device to main device (Global)
  - [ ] LLM as a service (Jetson)
  - [ ] Speech detection as a service (Jetson)
  - [ ] Speech as a service (Jetson)
  - [ ] Memory as a service (Jetson)
  - [ ] Vision as a service (Raspberry Pi)
  - [ ] Face as a service (Raspberry Pi)
  - [ ] Main loop (Jetson)
- [ ] Integrate Nvidia Jetson Orin Nano Super 8GB
- [ ] Integrate Hailo 10 as inference station (Llama 3.2 3b)
- [ ] Advanced voice: Move to ElevenLabs advanced voices.
- [ ] Tool use
  - [ ] Add frameqork for actions:
  - [ ] Open live camera feed action
  - [ ] Snap a picture
- [ ] Add aec for voice recognition from https://gist.github.com/thewh1teagle/929af1c6b05d5f96ceef01130e758471
- [ ] Introspection: Add Introspection agent for active and background thinking and processing.
- [ ] Growth: Add nightly finetuning, move to smaller model.

### Notes

While this is still my goal, you may see lower progress. 
This is becuase I have moved local AI development and help maintain jetson-containers.  
I still drive lower cost smart AI with personality, and it is easier on Pi and 3rd party models, but a true AI companion must be local AI.  

I also publish under org TeaBranch:
- [open-responses-server](https://github.com/teabranch/open-responses-server) for mcp support on chat-completions (as responses api and chat completions api) and all OpenAI's responses features
- [agentic-developer-mcp](https://github.com/teabranch/agentic-developer-mcp) for an agentic developer served as mcp that can work with other agentic developers, with agents as code.
- [agentic-code-indexer](https://github.com/teabranch/agentic-code-indexer) for indexing code for the agentic-developer-mcp
- [simple-semantic-chunker](https://github.com/teabranch/simple-semantic-chunker) for simple rag over documents

Join our Jetson AI Homelab discord community to talk more 

-nachos

## Prerequisites

Tau should be able to run on any linux with internet, but was tested only on a raspberry pi 5 8GB with official OS 64bit.  
Raspberry AI Kit is needed for vision (Can be disabled in code - configuration support per request/in future) 

### Keys
All needed keys are in .env_sample.  
Copy it to .env and add your keys.  
Currently, the main key is OpenAI (Chat, Speech, Whisper), and VoyageAI + Pinecone is for vectordb

I plan on moving back to Anthropic (3.5 sonnet only)

Groq was used for a fast understand action usecase

## Jetson Orin Nano Setup (JetPack 6.2)

This section provides complete setup instructions for running Tau on NVIDIA Jetson Orin Nano with JetPack 6.2 and Docker.

### Prerequisites for Jetson

- **NVIDIA Jetson Orin Nano** (8GB recommended)
- **JetPack 6.2** installed
- **Docker** with NVIDIA Container Toolkit
- **Internet connection** for downloading models

### Quick Start (Docker - Recommended)

#### 1. Clone the Repository
```bash
git clone https://github.com/OriNachum/autonomous-intelligence.git
cd autonomous-intelligence
```

#### 2. Configure Environment
```bash
# Copy environment template
cp baby-tau/.env_example .env

# Edit configuration for Jetson
nano .env
```

**Key settings for Jetson Orin Nano 8GB:**
```bash
# Port Configuration
SPEACHES_HOST_PORT=8001
VLLM_PORT=8000
KOKORO_TTS_HOST_PORT=8880

# Model Configuration (optimized for 8GB)
VLLM_MODEL=ibm-granite/granite-3.1-8b-instruct
OLLAMA_MODEL=llama3.2:1b

# Memory Settings
VLLM_GPU_MEMORY_UTILIZATION=0.30
VAD_EVERY_N_CHUNKS=6

# Voice Settings
TTS_VOICE=af_alloy

# Hugging Face Token (required for gated models)
HF_TOKEN=your_huggingface_token_here
```

#### 3. Start the Chat Agent
```bash
# Start all services with Docker
docker-compose -f baby-tau/docker-compose.yaml up -d

# Check if services are running
docker-compose -f baby-tau/docker-compose.yaml ps

# View logs
docker-compose -f baby-tau/docker-compose.yaml logs -f
```

#### 4. Run the Main Application
```bash
# For voice interaction
cd baby-tau/jetson
python3 main.py --audio

# For text interaction
python3 main.py
```

### Manual Setup (Alternative)

If Docker setup fails, follow these manual installation steps:

#### 1. Install System Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install audio dependencies
sudo apt-get install -y portaudio19-dev python3-all-dev python3-setuptools
sudo apt-get install -y espeak espeak-data libespeak-dev
sudo apt-get install -y alsa-utils pulseaudio

# Install build tools
sudo apt-get install -y build-essential cmake git pkg-config
```

#### 2. Install PyTorch for Jetson
```bash
# Install cuSPARSELt (required for PyTorch)
wget https://developer.download.nvidia.com/compute/cusparselt/0.6.3/local_installers/cusparselt-local-tegra-repo-ubuntu2204-0.6.3_1.0-1_arm64.deb
sudo dpkg -i cusparselt-local-tegra-repo-ubuntu2204-0.6.3_1.0-1_arm64.deb
sudo cp /var/cusparselt-local-tegra-repo-ubuntu2204-0.6.3/cusparselt-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install libcusparselt0 libcusparselt-dev

# Install PyTorch for Jetson
wget https://developer.download.nvidia.com/compute/redist/jp/v61/pytorch/torch-2.5.0a0+872d972e41.nv24.08.17622132-cp310-cp310-linux_aarch64.whl
pip3 install torch-2.5.0a0+872d972e41.nv24.08.17622132-cp310-cp310-linux_aarch64.whl

# Set up environment
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# Create symbolic link
sudo ln -sf /usr/local/cuda/lib64/libcusparse.so.12 /usr/local/cuda/lib64/libcusparse.so
```

#### 3. Install Python Dependencies
```bash
cd jetson-super
chmod +x setup.sh
./setup.sh

# Install additional requirements
cd ../baby-tau/jetson
pip3 install -r ../../jetson-4gb-legacy/requirements.txt
```

#### 4. Configure and Run
```bash
# Copy environment template
cp ../../baby-tau/.env_example .env

# Edit configuration
nano .env

# Start services manually (in separate terminals)
# Terminal 1: Start STT service
python3 services/speech_transcriber.py

# Terminal 2: Start LLM service
python3 services/ollama_service.py

# Terminal 3: Start TTS service
python3 services/speaker.py

# Terminal 4: Start main application
python3 main.py --audio
```

### Service Architecture

The system runs with the following services:

1. **Speech-to-Text (STT)** - Port 8001
   - Uses faster-whisper for local speech recognition
   - Handles audio input and transcription

2. **Large Language Model (LLM)** - Port 8000
   - Runs local models (Llama, Gemma, Granite)
   - Processes conversation and generates responses

3. **Text-to-Speech (TTS)** - Port 8880
   - Converts text responses to audio
   - Supports multiple TTS engines (Piper, Kokoro)

4. **Main Application**
   - Coordinates all services
   - Handles voice activity detection (VAD)
   - Manages conversation flow

### Troubleshooting

#### Common Issues and Solutions

**1. CUDA not detected:**
```bash
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
python3 -c "import torch; print(f'CUDA version: {torch.version.cuda}')"
```

**2. Audio device issues:**
```bash
# Check audio devices
aplay -l
arecord -l

# Start PulseAudio
pulseaudio --start

# Test audio
speaker-test -t wav -c 2
```

**3. Memory issues:**
- Reduce `VLLM_GPU_MEMORY_UTILIZATION` to 0.2-0.3
- Use smaller models like `llama3.2:1b`
- Increase `VAD_EVERY_N_CHUNKS` to 8-10

**4. Camera issues (if using vision):**
```bash
# Check camera devices
ls -la /dev/video*
v4l2-ctl --list-devices
```

**5. Docker permission issues:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in, or run:
newgrp docker
```

### Performance Optimization

For optimal performance on Jetson Orin Nano 8GB:

- **Power Mode:** Set to MAXN (maximum performance)
- **Memory:** Use 30% GPU memory for VLLM
- **Models:** Start with smaller models (1B parameters)
- **VAD:** Increase chunk processing interval to reduce CPU load
- **Cooling:** Ensure adequate cooling for sustained performance

### Usage

Once running, the system will:

1. **Listen** for voice input using VAD (Voice Activity Detection)
2. **Transcribe** speech to text using Whisper
3. **Process** with local LLM (Llama/Gemma/Granite)
4. **Synthesize** response using TTS
5. **Play** audio response

**Voice Commands:**
- Speak naturally - the system uses VAD to detect when you start/stop talking
- The system maintains conversation context
- Use Ctrl+C to exit

**Text Mode:**
- Type messages and press Enter
- Type `/q` to quit

## Installation

1. Cloning Git repositories
1.1. Clone this repository to your Raspberry Pi:

```
git clone https://github.com/OriNachum/autonomous-intelligence.git
```

1.2. Clone this repository to your Raspberry Pi:
```
git clone https://github.com/OriNachum/hailo-rpi5-examples.git
```
I have a pending PR to integrate this to main repo.
```
https://github.com/hailo-ai/hailo-rpi5-examples/pull/50
```
If you do, set up the your machine for Hailo-8L chip per Hailo's instructions.


2. Copy .env_sample to .env and add all keys:
- ANTHROPIC_API_KEY: used for Claude based text completion and vision. Currently unused.
- OPENAI_API_KEY: Used for Speech, Whisper, vision and text.
- GROQ_API_KEY: Used for a super quick action understanding, May be replaced with embeddings.
- VOYAGE_API_KEY: VoyageAI is recommended by Anthropic. They offer the best embeddings to date (of when I selected it), and offer a great option for innovators.
- PINECONE_API_KEY: API Key of pinecone. Serverless is a great option.
- PINECONE_DIMENSION: Dimension of the embeddings generated by Voyage. Used for the setup of Pinecone
- PINECONE_INDEX_NAME: Name of the index in Pinecone, for memory

## Usage

There are five programs to run by this order:
1. hailo-rpi5-examples:
  1. basic-pipelines/detection_service.py: This runs the camera and emits events on changes on detection 
2. autonomous-intelligence
  1. services/face_service.py: this starts the face app, and reacts when speech occurs
  2. tau.py: this is the main LLM conversation loop
  3. tau_speech.py: this consumes speech events, and produces actual speech
  4. services/microphone_listener.py this listens to your speech and emits events to tau.py as input

## Acknowledgements

There are multiple people for which I want to acknowledge for this development.  
Of them, these are the people who confirmed for me to mention them: 
- @Sagigamil 
  
## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=OriNachum/autonomous-intelligence&type=Date)](https://www.star-history.com/#OriNachum/autonomous-intelligence&Date)

⸻

## License

This project is licensed under the [MIT License](LICENSE).
