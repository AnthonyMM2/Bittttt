import discord
from discord import app_commands
import json
import subprocess
import os

# ==============================
# CONFIGURACIÓN
# ==============================

TOKEN = "MTQ3Mzg2OTMxMjAyMzU5NzE3Mg.GCJqNM.Xw3vLcYoBJZuZCMsfsM8zpTrC82ULyZKKm3Sow"
META_FILE = "meta.json"
GIT_MSG = "Update meta.json 💰"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ==============================
# ARCHIVO JSON
# ==============================

def cargar_datos():
    if not os.path.exists(META_FILE):
        datos = {"meta": 100, "actual": 0}
        guardar_datos(datos)
        return datos

    with open(META_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(datos):
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2)

# ==============================
# GIT PUSH
# ==============================

def push_github():
    try:
        subprocess.run(["git", "add", META_FILE], check=True)
        subprocess.run(["git", "commit", "-m", GIT_MSG], check=True)
        subprocess.run(["git", "push"], check=True)
        return True
    except:
        return False

# ==============================
# EVENTO READY
# ==============================

@client.event
async def on_ready():
    await tree.sync()
    print(f"Conectado como {client.user}")

# ==============================
# /meta
# ==============================

@tree.command(name="meta", description="Establecer nueva meta")
async def meta(interaction: discord.Interaction, cantidad: float):
    datos = cargar_datos()
    datos["meta"] = cantidad
    guardar_datos(datos)

    push_ok = push_github()

    msg = (
        f"🔥 NUEVA META CONFIGURADA\n"
        f"🎯 Meta: {cantidad} USD\n"
        f"💰 Recaudado: {datos['actual']} USD"
    )

    if push_ok:
        msg += "\n✅ Web actualizada"

    await interaction.response.send_message(msg)

# ==============================
# /donar
# ==============================

@tree.command(name="donar", description="Registrar donación")
async def donar(interaction: discord.Interaction, cantidad: float):
    datos = cargar_datos()
    datos["actual"] += cantidad
    guardar_datos(datos)

    porcentaje = (datos["actual"] / datos["meta"]) * 100 if datos["meta"] > 0 else 0
    push_ok = push_github()

    msg = (
        f"💰 DONACIÓN RECIBIDA\n"
        f"➕ +{cantidad} USD\n"
        f"🔥 Total: {datos['actual']} USD\n"
        f"📊 Progreso: {porcentaje:.2f}%"
    )

    if push_ok:
        msg += "\n✅ Web actualizada"

    await interaction.response.send_message(msg)

client.run(TOKEN)
