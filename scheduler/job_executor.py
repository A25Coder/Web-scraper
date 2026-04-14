from .utils import export_data, send_email_notification
import subprocess
import sys
import json
import tempfile
import os


def execute_job(job, timeout: int = 300):
    print(f"🚀 Running Job: {job.job_id}")

    try:
        # run scraping in a completely separate Python process via the CLI worker
        # Run the worker as a module so Python sets sys.path to project root
        project_root = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))
        env = os.environ.copy()
        env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")

        worker_module = "scraper.scraping_worker"
        cmd = [sys.executable, "-m", worker_module, "--url", job.target_url, "--query", job.query]

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=project_root, env=env)

        if proc.returncode != 0:
            stderr = proc.stderr.strip()
            raise RuntimeError(f"Scraping worker failed: {stderr}")

        # parse stdout as JSON, fallback to raw string
        try:
            result = json.loads(proc.stdout)
        except Exception:
            result = proc.stdout

        # honor max_rows if the result is a list-like
        try:
            max_rows = int(getattr(job, "max_rows", 0) or 0)
        except Exception:
            max_rows = 0

        if max_rows and isinstance(result, (list, tuple)):
            result = result[:max_rows]

        export_data(result, job)

        # update app cache so the Streamlit dashboard shows latest results
        try:
            from app.utils.cache_manager import save_cache

            save_cache(job.target_url, {"final_output": result, "extracted_data": []}, job.query)
        except Exception:
            # best-effort: do not fail the job if cache update isn't available
            pass

        if getattr(job, "email_notification", False):
            send_email_notification(job)

    except subprocess.TimeoutExpired:
        print("❌ Job Failed: Scraping timed out")
    except Exception as e:
        print(f"❌ Job Failed: {e}")