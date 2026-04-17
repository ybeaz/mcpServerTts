import subprocess
import json


from shared.getItPrinted import getItPrinted as PRINT, comment, EXIT


def get_duration_seconds(file_path):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            file_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


if __name__ == "__main__":
    """
    Import: from shared.getDurationSeconds import getDurationSeconds
    Run: Terminal > `python -m shared.getDurationSeconds`
    """
    output = get_duration_seconds("./__output__/output4.wav")

    PRINT(output, comment())
