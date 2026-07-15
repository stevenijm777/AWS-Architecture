import csv
import re
from pathlib import Path

def parse_videos():
    input_path = Path("videos.txt")
    output_path = Path("videos.csv")
    
    if not input_path.exists():
        print(f"Error: {input_path} not found.")
        return

    # Build a title -> video_id map from existing videos.csv if available
    video_id_map = {}
    if output_path.exists():
        try:
            with open(output_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "title" in row and "video_id" in row:
                        video_id_map[row["title"].strip()] = row["video_id"].strip()
        except Exception as e:
            print(f"Warning: Could not read existing videos.csv: {e}")

    content = input_path.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines()]
    
    videos = []
    
    i = 0
    while i < len(lines):
        # Skip empty lines
        if not lines[i]:
            i += 1
            continue
            
        # Check if the line is a number (start of a video block)
        if re.match(r"^\d+$", lines[i]):
            try:
                vid_id = lines[i]
                # Safely read the next lines of the block
                is_true = lines[i+1]
                duration = lines[i+2]
                status = lines[i+3]
                title = lines[i+4]
                publisher = lines[i+5]
                bullet = lines[i+6]
                views_age_line = lines[i+7]
                
                # Split views and age by the bullet point separator
                views = ""
                age = ""
                if "•" in views_age_line:
                    parts = views_age_line.split("•")
                    views = parts[0].strip()
                    age = parts[1].strip()
                else:
                    views = views_age_line.strip()
                
                # Retrieve existing video_id if available
                youtube_id = video_id_map.get(title.strip(), "")
                
                videos.append({
                    "id": vid_id,
                    "title": title,
                    "duration": duration,
                    "views": views,
                    "age": age,
                    "video_id": youtube_id
                })
                i += 8
            except IndexError:
                # File is truncated
                break
        else:
            i += 1
            
    # Write to CSV
    with open(output_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "duration", "views", "age", "video_id"])
        writer.writeheader()
        writer.writerows(videos)
        
    print(f"Successfully parsed {len(videos)} videos and saved to {output_path}")

if __name__ == "__main__":
    parse_videos()
