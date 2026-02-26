#!/usr/bin/env python3
"""
🛡️ MINECRAFT PORT SCANNER Made By Sina_Ahmadi (Kurdistan)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import socket
import threading
import time
import json
import os
from datetime import datetime
import subprocess

class MinecraftPortScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ MineCraft Port Scanner | Made By Sina_Ahmadi")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0d1117")
        self.root.resizable(True, True)
        
        self.scanning = False
        self.results = []
        self.open_ports = []
        
        self.minecraft_ports = [25565, 19132, 25566, 25575, 7777, 25555, 30000, 40000, 4711]
        
        self.setup_gui()
    
    def setup_gui(self):
        # Header
        header = tk.Label(self.root, text="⚡ MineCraft Port Scanner Made By Sina_Ahmadi ⚡", 
                         font=("Consolas", 24, "bold"), fg="#ff6b35", bg="#0d1117")
        header.pack(pady=20)
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg="#0d1117")
        input_frame.pack(pady=20, padx=50, fill=tk.X)
        
        tk.Label(input_frame, text="🎮 Server IP:", font=("Consolas", 16, "bold"), 
                fg="#00ff88", bg="#0d1117").pack(anchor=tk.W)
        
        self.ip_entry = tk.Entry(input_frame, font=("Consolas", 14), width=40, 
                                bg="#161b22", fg="#00ff88", insertbackground="#00ff88",
                                relief=tk.FLAT, bd=3)
        self.ip_entry.pack(fill=tk.X, pady=(5,15))
        self.ip_entry.insert(0, "play.hypixel.net")
        
        # Port Range
        range_frame = tk.Frame(self.root, bg="#0d1117")
        range_frame.pack(pady=10, padx=50, fill=tk.X)
        
        tk.Label(range_frame, text="🔍 Port Range:", font=("Consolas", 14), 
                fg="#ffaa00", bg="#0d1117").pack(anchor=tk.W)
        
        range_input = tk.Frame(range_frame, bg="#0d1117")
        range_input.pack(fill=tk.X)
        
        self.start_port = tk.Entry(range_input, font=("Consolas", 12), width=10, 
                                  bg="#161b22", fg="#ffaa00")
        self.start_port.pack(side=tk.LEFT)
        self.start_port.insert(0, "1")
        
        tk.Label(range_input, text=" ➜ ", font=("Consolas", 16), fg="#ffaa00", 
                bg="#0d1117").pack(side=tk.LEFT, padx=5)
        
        self.end_port = tk.Entry(range_input, font=("Consolas", 12), width=10, 
                                bg="#161b22", fg="#ffaa00")
        self.end_port.pack(side=tk.LEFT)
        self.end_port.insert(0, "65535")
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg="#0d1117")
        btn_frame.pack(pady=30)
        
        self.scan_btn = tk.Button(btn_frame, text="🚀 Scan Now", font=("Consolas", 16, "bold"), 
                                 bg="#ff6b35", fg="white", width=20, height=2,
                                 command=self.start_scan, relief=tk.FLAT)
        self.scan_btn.pack(side=tk.LEFT, padx=15)
        
        self.quick_btn = tk.Button(btn_frame, text="⚡ MC QUICK SCAN", font=("Consolas", 14, "bold"), 
                                  bg="#00ff88", fg="black", width=18, height=2,
                                  command=self.quick_mc_scan, relief=tk.FLAT)
        self.quick_btn.pack(side=tk.LEFT, padx=15)
        
        self.save_btn = tk.Button(btn_frame, text="💾 SAVE REPORT", font=("Consolas", 14, "bold"), 
                                 bg="#5865f2", fg="white", width=16, height=2,
                                 command=self.save_report, relief=tk.FLAT, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=15)
        
        # Progress
        self.progress = ttk.Progressbar(self.root, mode='determinate', length=800)
        self.progress.pack(pady=20)
        
        self.status_label = tk.Label(self.root, text="🟢 READY - Enter IP and HUNT PORTS!", 
                                    font=("Consolas", 14), fg="#00ff88", bg="#0d1117")
        self.status_label.pack()
        
        # Results
        self.results_text = scrolledtext.ScrolledText(self.root, bg="#0f0f23", fg="#00ff88",
                                                     font=("Consolas", 11), wrap=tk.WORD,
                                                     insertbackground="#00ff88", height=20)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        # Summary
        self.summary_label = tk.Label(self.root, text="Summary appears here...", 
                                     font=("Consolas", 12), fg="#ff6b35", bg="#0d1117")
        self.summary_label.pack(pady=10)
    
    def update_status(self, msg, color="#00ff88"):
        self.status_label.config(text=msg, fg=color)
        self.root.update()
    
    def start_scan(self):
        ip = self.ip_entry.get().strip()
        if not ip or not self.validate_ip(ip):
            messagebox.showerror("❌ Error", "Invalid IP address!")
            return
        
        self.scanning = True
        self.results = []
        self.open_ports = []
        self.results_text.delete(1.0, tk.END)
        
        self.scan_btn.config(state=tk.DISABLED, text="🔄 SCANNING...")
        self.quick_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        
        start_port = int(self.start_port.get())
        end_port = int(self.end_port.get())
        
        thread = threading.Thread(target=self.scan_ports, args=(ip, start_port, end_port))
        thread.daemon = True
        thread.start()
    
    def quick_mc_scan(self):
        """Quick scan common Minecraft ports"""
        ip = self.ip_entry.get().strip()
        if not ip:
            return
        
        self.scanning = True
        self.results_text.delete(1.0, tk.END)
        self.scan_btn.config(state=tk.DISABLED)
        self.quick_btn.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.scan_mc_ports, args=(ip,))
        thread.daemon = True
        thread.start()
    
    def validate_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except:
            return False
    
    def scan_ports(self, ip, start_port, end_port):
        total_ports = end_port - start_port + 1
        self.progress['maximum'] = total_ports
        self.progress['value'] = 0
        
        self.update_status(f"🔍 Scanning {ip}:{start_port}-{end_port}", "#ffaa00")
        
        for port in range(start_port, end_port + 1):
            if not self.scanning:
                break
            
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                
                if result == 0:
                    service = self.get_service_name(port)
                    self.open_ports.append({"port": port, "service": service})
                    self.log_result(f"✅ OPEN", port, service, f"{ip}:{port}")
                
                sock.close()
                self.progress['value'] += 1
                self.root.update()
                
            except:
                pass
        
        self.scan_finished()
    
    def scan_mc_ports(self, ip):
        """Scan common Minecraft ports"""
        self.progress['maximum'] = len(self.minecraft_ports)
        self.progress['value'] = 0
        
        self.update_status(f"⚡ Quick MC Scan: {ip}", "#00ff88")
        self.results_text.insert(tk.END, f"🎮 MINECRAFT QUICK SCAN - {ip}\n")
        self.results_text.insert(tk.END, "="*60 + "\n\n")
        
        for i, port in enumerate(self.minecraft_ports):
            if not self.scanning:
                break
            
            service = "Minecraft/Java" if port == 25565 else "Bedrock/Other"
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                result = sock.connect_ex((ip, port))
                
                if result == 0:
                    self.open_ports.append({"port": port, "service": service})
                    self.log_result(f"✅ MINECRAFT", port, service, f"{ip}:{port}")
                else:
                    self.results_text.insert(tk.END, f"❌ CLOSED  {port:5d}  {service}\n")
                
                sock.close()
            except:
                self.results_text.insert(tk.END, f"❌ TIMEOUT {port:5d}  {service}\n")
            
            self.progress['value'] = i + 1
            self.root.update()
            time.sleep(0.1)
        
        self.scan_finished()
    
    def log_result(self, status, port, service, target):
        timestamp = time.strftime("%H:%M:%S")
        result = f"[{timestamp}] {status:<10} {port:5d}  {service:<20}  {target}\n"
        
        self.results.append({
            "timestamp": timestamp,
            "status": status,
            "port": port,
            "service": service,
            "target": target
        })
        
        self.root.after(0, lambda r=result: self.results_text.insert(tk.END, r))
        self.root.after(0, lambda: self.results_text.see(tk.END))
    
    def get_service_name(self, port):
        common_services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 993: "IMAPS", 995: "POP3S",
            25565: "Minecraft", 19132: "Bedrock"
        }
        return common_services.get(port, "Unknown")
    
    def scan_finished(self):
        self.scanning = False
        self.scan_btn.config(state=tk.NORMAL, text="🚀 FULL SCAN")
        self.quick_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
        self.progress.stop()
        
        summary = f"✅ SCAN COMPLETE! Found {len(self.open_ports)} open ports"
        self.update_status(summary, "#00ff88")
        self.show_summary()
    
    def show_summary(self):
        if not self.open_ports:
            self.summary_label.config(text="❌ No open ports found", fg="#ff4444")
            return
        
        mc_count = sum(1 for p in self.open_ports if p["port"] in self.minecraft_ports)
        summary = f"🎮 MINECRAFT PORTS: {mc_count} | TOTAL OPEN: {len(self.open_ports)}"
        self.summary_label.config(text=summary, fg="#00ff88")
    
    def save_report(self):
        if not self.open_ports:
            messagebox.showinfo("Info", "No results to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON", "*.json"), ("All", "*.*")],
            initialname=f"minecraft_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            if filename.endswith('.json'):
                with open(filename, 'w') as f:
                    json.dump({
                        "scan_info": {
                            "target": self.ip_entry.get(),
                            "timestamp": datetime.now().isoformat(),
                            "total_open": len(self.open_ports)
                        },
                        "open_ports": self.open_ports
                    }, f, indent=2)
            else:
                with open(filename, 'w') as f:
                    f.write(f"MINECRAFT PORT SCAN REPORT\n")
                    f.write(f"Target: {self.ip_entry.get()}\n")
                    f.write(f"Date: {datetime.now()}\n")
                    f.write("="*60 + "\n\n")
                    
                    for port_info in self.open_ports:
                        f.write(f"PORT {port_info['port']:5d} - {port_info['service']}\n")
            
            messagebox.showinfo("✅ Saved!", f"Report saved to:\n{filename}")
    
    def on_closing(self):
        self.scanning = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftPortScanner(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()