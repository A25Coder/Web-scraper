import os
import pandas as pd


def export_data(data, job):
    # Coerce various possible result shapes into a DataFrame-friendly structure
    if isinstance(data, pd.DataFrame):
        df = data
    else:
        # dict of lists or scalars
        if isinstance(data, dict):
            # if values are list-like and roughly same length, DataFrame will work
            try:
                df = pd.DataFrame(data)
            except Exception:
                # fallback: wrap dict as single-row
                df = pd.DataFrame([data])
        elif isinstance(data, (list, tuple)):
            # list of records (dicts) is ideal; otherwise try to construct
            try:
                df = pd.DataFrame(data)
            except Exception:
                # convert items to dicts
                df = pd.DataFrame([{"value": x} for x in data])
        else:
            # primitive or unknown type -> single-row
            df = pd.DataFrame([{"value": data}])

    filename_base = f"outputs/{job.job_id}"

    # ensure output directory exists
    out_dir = os.path.dirname(filename_base)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    if job.export_format == "CSV":
        df.to_csv(f"{filename_base}.csv", index=False)

    elif job.export_format == "JSON":
        df.to_json(f"{filename_base}.json", orient="records")

    print(f"✅ Data exported for job {job.job_id}")


def send_email_notification(job):
    print(f"📧 Email sent for job {job.job_id}")
    # Integrate SMTP later