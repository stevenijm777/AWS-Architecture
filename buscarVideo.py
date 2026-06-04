import pandas as pd
import sys
import os
from rich.console import Console
from rich.table import Table

def search_video(query=None):
    console = Console()
    csv_path = os.path.join(os.path.dirname(__file__), "videos.csv")
    
    if not os.path.exists(csv_path):
        console.print(f"[bold red]Error: No se encontró el archivo {csv_path}.[/bold red]")
        return
        
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        console.print(f"[bold red]Error al leer {csv_path}: {e}[/bold red]")
        return

    if not query:
        # Consulta por defecto solicitada por el usuario
        query = "Create Personalized Videos"
    
    console.print(f"[bold blue]Buscando videos que coincidan con:[/bold blue] '[bold yellow]{query}[/bold yellow]'\n")
    
    # Búsqueda insensible a mayúsculas/minúsculas usando pandas
    # Soporta buscar subcadenas o las primeras palabras
    results = df[df['title'].str.contains(query, case=False, na=False)]
    
    if results.empty:
        # Intentar una búsqueda más flexible con las primeras palabras
        words = query.split()
        if len(words) > 1:
            fallback_query = " ".join(words[:3])
            console.print(f"[yellow]No se encontraron resultados exactos. Intentando búsqueda con las primeras palabras:[/yellow] '[bold]{fallback_query}[/bold]'...")
            results = df[df['title'].str.contains(fallback_query, case=False, na=False)]

    if results.empty:
        console.print("[bold red]No se encontraron videos coincidentes.[/bold red]")
        return

    # Mostrar resultados en una tabla elegante
    table = Table(title="Resultados de Búsqueda de Videos", title_style="bold magenta")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Título", style="green")
    table.add_column("Duración", justify="center", style="white")
    table.add_column("Visualizaciones", justify="right", style="dim")
    table.add_column("Tiempo Publicado (Año)", justify="center", style="yellow")

    for _, row in results.iterrows():
        table.add_row(
            str(row['id']),
            str(row['title']),
            str(row['duration']),
            str(row['views']),
            str(row['age'])
        )
        
    console.print(table)

if __name__ == "__main__":
    search_term = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    search_video(search_term)
