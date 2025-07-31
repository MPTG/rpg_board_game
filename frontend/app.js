document.getElementById('loadDataButton').onclick = async () => {
    const addr = document.getElementById('address').value.trim();
    if (!addr) {
        alert('Please enter a valid address.');
        return;
    }
    try {
        const response = await fetch(`${backendUrl}/players?address=${encodeURIComponent(addr)}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('dataDisplay').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        document.getElementById('status').textContent = 'Error fetching data: ' + error.message;
    }
};

document.getElementById('resetViewedPlayers').onclick = async () => {
    try {
        const response = await fetch(`${backendUrl}/resetViewedPlayers`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        document.getElementById('status').textContent = 'Viewed players reset successfully.';
    } catch (error) {
        document.getElementById('status').textContent = 'Error resetting viewed players: ' + error.message;
    }
}
