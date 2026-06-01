import pandas as pd, os, glob

folder = r'c:\Users\laksh\Desktop\arista\cyber_final\cyber_final\archive (1)'
files = sorted(glob.glob(os.path.join(folder, '*.parquet')))

total_rows = 0
all_cols = None

with open(os.path.join(os.path.dirname(folder), 'dataset_check.txt'), 'w', encoding='utf-8') as out:
    out.write("CSE-CIC-IDS2018 DATASET AUDIT\n")
    out.write("=" * 80 + "\n\n")

    for f in files:
        df = pd.read_parquet(f)
        name = os.path.basename(f)
        size_mb = os.path.getsize(f) / (1024*1024)
        total_rows += len(df)

        # Check label column
        label_col = next((c for c in df.columns if c.lower().strip() == 'label'), None)
        if label_col:
            labels = df[label_col].value_counts()
        else:
            labels = "NO LABEL COLUMN FOUND"

        out.write(f"FILE: {name}\n")
        out.write(f"  Size     : {size_mb:.1f} MB\n")
        out.write(f"  Rows     : {len(df):,}\n")
        out.write(f"  Columns  : {len(df.columns)}\n")
        out.write(f"  Label col: {label_col}\n")
        out.write(f"  Labels   :\n")
        if isinstance(labels, str):
            out.write(f"    {labels}\n")
        else:
            for lbl, cnt in labels.items():
                out.write(f"    {str(lbl):30s} : {cnt:>10,}\n")
        out.write(f"  NaN count: {df.isnull().sum().sum():,}\n")
        out.write(f"  Inf count: {df.select_dtypes('number').apply(lambda s: s.isin([float('inf'), float('-inf')]).sum()).sum():,}\n")
        out.write("\n")

        if all_cols is None:
            all_cols = set(df.columns)
        else:
            if set(df.columns) != all_cols:
                out.write(f"  WARNING: Column mismatch vs first file!\n")
                out.write(f"    Missing: {all_cols - set(df.columns)}\n")
                out.write(f"    Extra:   {set(df.columns) - all_cols}\n\n")

    out.write("=" * 80 + "\n")
    out.write(f"TOTAL FILES : {len(files)}\n")
    out.write(f"TOTAL ROWS  : {total_rows:,}\n")
    out.write(f"TOTAL SIZE  : {sum(os.path.getsize(f) for f in files)/(1024*1024*1024):.2f} GB\n")
    out.write(f"COLUMNS     : {len(all_cols)}\n")

print("Done! Check dataset_check.txt")
