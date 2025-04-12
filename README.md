# Lynn AI

A terminal-based AI assistant specialized in drug delivery systems for tumor targeting with extensive chemistry knowledge.

## Features

- Interactive command-line interface
- Text messaging interface
- Web API for integration with other applications
- Chemistry knowledge focused on drug delivery and tumor targeting
- Web search capabilities for latest research information
- Conversational responses mimicking human expert interaction

## Requirements

- Python 3.8+
- OpenAI API key

## Installation

1. Clone or download this repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key (use `.env.example` as a template)
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file to add your OpenAI API key

## Usage Options

### Terminal Mode

Run the application in a terminal with:

```
./run.sh
```

### Text Messaging Mode

1. First, start the API server in one terminal:
   ```
   ./run_api.sh
   ```

2. Then, start the text messaging client in another terminal:
   ```
   ./text.sh
   ```

### API Mode

Start the API server and access it via HTTP requests:

```
./run_api.sh
```

The API will be available at http://localhost:5000.

## Commands

- Type your questions or topics related to drug delivery and tumor targeting
- Type `exit`, `quit`, or `bye` to end the session

## Example Questions

- "What are the main challenges in delivering hydrophobic drugs to solid tumors?"
- "Explain the EPR effect in nanoparticle drug delivery"
- "How do pH-responsive polymers work in targeted drug delivery?"
- "What are the latest advancements in liposomal drug delivery for cancer?"
- "Compare active vs passive targeting mechanisms for tumor drug delivery" 