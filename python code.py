from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- MATHEMATICAL ENGINE FUNCTIONS ---

def local_execution_energy(cpu_cycles, energy_per_cycle=0.0005):
    """
    Calculates energy consumed for processing a task locally on an IoT device.
    """
    return cpu_cycles * energy_per_cycle


def offloading_energy(task_size, transmission_energy=0.0003):
    """
    Calculates energy consumed for transmitting/offloading a task to an edge server.
    """
    return task_size * transmission_energy


def total_latency(network_latency, edge_latency):
    """
    Calculates the total round-trip latency when a task is offloaded.
    """
    return network_latency + edge_latency


def decide_offloading(task_size, cpu_cycles, network_latency, edge_latency):
    """
    Core decision engine: selects the execution mode that minimizes energy 
    consumption while satisfying latency constraints.
    """
    local_energy = local_execution_energy(cpu_cycles)
    offload_energy = offloading_energy(task_size)
    offload_latency = total_latency(network_latency, edge_latency)

    # Threshold condition matching project specifications (latency <= 100ms)
    if offload_energy < local_energy and offload_latency <= 100:
        return {
            "decision": "OFFLOAD TO EDGE SERVER",
            "energy": round(offload_energy, 4),
            "latency": round(offload_latency, 2)
        }
    else:
        return {
            "decision": "EXECUTE LOCALLY ON IOT DEVICE",
            "energy": round(local_energy, 4),
            "latency": 0
        }

# --- ROUTES ---

@app.route("/")
def index():
    """Renders the main web dashboard interface."""
    return render_template("index.html")


@app.route("/offload", methods=["POST"])
def offload():
    """API endpoint to receive metrics and return the offloading decision."""
    data = request.json
    try:
        task_size = float(data["task_size"])
        cpu_cycles = float(data["cpu_cycles"])
        network_latency = float(data["network_latency"])
        edge_latency = float(data["edge_latency"])
        
        result = decide_offloading(task_size, cpu_cycles, network_latency, edge_latency)
        return jsonify(result)
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input data standard"}), 400


if __name__ == "__main__":
    # Running in debug mode as specified in the implementation design
    app.run(debug=True)
