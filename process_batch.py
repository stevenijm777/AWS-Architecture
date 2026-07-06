import argparse
import pandas as pd
import subprocess
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Process batch of AWS Architecture videos")
    parser.add_argument(
        "--force", action="store_true",
        help="Force processing of videos, ignoring existing graphs and cached analysis",
    )
    parser.add_argument(
        "--force-vision", action="store_true",
        help="Force vision analysis, ignoring cached vision analysis and existing graphs, but reusing transcripts",
    )
    args = parser.parse_args()

    csv_path = "videos.csv"
    if not os.path.exists(csv_path):
        print(f"No se encontró {csv_path}")
        return

    df = pd.read_csv(csv_path)
    # Reverse the DataFrame to process the oldest videos first, and reset the index
    df = df.iloc[::-1].reset_index(drop=True)
    print("Iniciando procesamiento por lotes...")
    
    for index, row in df.iterrows():
        title = row['title']
        
        # Skip special, compilation, or long videos (> 12 minutes)
        title_lower = title.lower()
        duration_str = str(row['duration'])
        is_special = False
        if any(k in title_lower for k in ["spotlight", "greatest hits", "bloopers", "reprise", "(special)", "(special episode)"]):
            is_special = True
        else:
            try:
                parts = duration_str.strip().split(":")
                if len(parts) == 2:
                    minutes = int(parts[0])
                elif len(parts) == 3:
                    minutes = int(parts[0]) * 60 + int(parts[1])
                else:
                    minutes = 0
                if minutes >= 12:
                    is_special = True
            except Exception:
                pass
                
        if is_special:
            print(f"Saltando video especial/recopilación/largo: {title}")
            continue

        print(f"\n[{index+1}/{len(df)}] Buscando: {title}")
        
        try:
            # Check if video_id is already in the CSV
            video_id = None
            if "video_id" in row and pd.notna(row["video_id"]) and str(row["video_id"]).strip():
                video_id = str(row["video_id"]).strip()
                print(f"Video ID (desde CSV): {video_id}")
            else:
                # Buscar el ID del video
                query = f"AWS Architecture {title}"
                result = subprocess.run(
                    ["yt-dlp", "--get-id", f"ytsearch1:{query}"], 
                    capture_output=True, text=True, check=True
                )
                video_id = result.stdout.strip().split('\n')[0]
            
            if not video_id:
                print("No se encontró el ID.")
                continue
                
            print(f"Video ID encontrado: {video_id}")
            
            # Verificar si ya existe el grafo
            graph_file = f"data/graphs/{video_id}.graphml"
            if os.path.exists(graph_file) and not args.force and not args.force_vision:
                print(f"El video {video_id} ya fue procesado previamente. Saltando...")
                continue
                
            # Ejecutar el pipeline
            url = f"https://www.youtube.com/watch?v={video_id}"
            print(f"Iniciando pipeline para {url}...")
            
            cmd = [".venv/bin/python", "main.py", "--url", url]
            if args.force:
                cmd.append("--force")
            elif args.force_vision:
                cmd.append("--force-vision")
            pipeline_result = subprocess.run(cmd)
            
            if pipeline_result.returncode != 0:
                print(f"\n[!] El pipeline falló para {video_id}. Es probable que se haya agotado la cuota de la API gratuita (503/429).")
                print("Deteniendo el proceso por lotes para no saturar...")
                break
                
        except subprocess.CalledProcessError as e:
            print(f"Error al buscar yt-dlp para {title}: {e}")
        except Exception as e:
            print(f"Error general procesando {title}: {e}")

    print("\nProcesamiento por lotes finalizado o detenido.")

if __name__ == "__main__":
    main()
