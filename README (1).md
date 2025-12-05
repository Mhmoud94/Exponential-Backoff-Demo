# Exponential Backoff Demo 📡

An interactive Python visualization tool demonstrating **Exponential Backoff** — a smart retry strategy used in distributed systems and network applications.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## What is Exponential Backoff?

Instead of immediately retrying a failed request, the system waits progressively longer between each attempt:

```
1s → 2s → 4s → 8s → 16s → ...
```

This prevents overwhelming a struggling server and significantly increases the chance of successful recovery.

## Features

- **Side-by-Side Comparison**: See the difference between retry strategies with and without backoff
- **Exponential Graph**: Visualize how wait times grow with each attempt
- **Jitter Visualization**: Understand how randomness prevents the "thundering herd" problem
- **Server Load Simulation**: Watch how different numbers of clients affect server performance
- **Adjustable Parameters**: Customize base wait time, max attempts, number of clients, and simulation speed

## Demo Modes

| Mode | Description |
|------|-------------|
| **Comparison** | Side-by-side view of backoff vs. no backoff |
| **Without Backoff** | Shows what happens with immediate retries |
| **With Backoff** | Demonstrates exponential wait times |
| **With Jitter** | Adds randomness to spread out retries |
| **Graph** | Visualizes exponential growth curve |

## Installation

```bash
# Clone the repository
git clone https://github.com/Mhmoud94/exponential-backoff.git
cd exponential-backoff

# Run the demo (requires Python 3.7+ with tkinter)
python Exponential_Backoff.py
```

## Requirements

- Python 3.7+
- tkinter (usually included with Python)

## Usage

1. Run the script
2. Select a demo mode from the control panel
3. Adjust parameters (base wait time, max attempts, number of clients)
4. Click **Start Demo** to begin the visualization
5. Watch the log panel for detailed retry information

## Real-World Applications

Exponential backoff is used by major tech companies including:

- **Google Cloud**: Built into official client libraries for handling HTTP 429/503 errors
- **AWS**: Recommended strategy for API rate limiting
- **TCP/IP**: Used in network congestion control

## Key Concepts

- **Base Wait**: Initial delay before first retry
- **Max Attempts**: Maximum number of retry attempts
- **Jitter**: Random delay added to prevent synchronized retries
- **Thundering Herd**: Problem where many clients retry simultaneously after a failure

## Leadership Insight

The algorithm mirrors real-world resilience:
- Give space after setbacks
- Pace work to prevent burnout
- Retry smarter, not harder

## Team

**Group H** — Dalarna University, Data-Driven Leadership Course

Mhmoud Ahmad, Minni Helena, Ashok Enukonda, Linh Nguyen, Subin Parappan, Abeer Aman, Medha Phatak

## License

MIT License — feel free to use and modify for your own projects.
