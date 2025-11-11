def process_ranap_data(input_csv_path, output_csv_path='final_extracted_ranap_data.csv'):
    import pandas as pd
    import numpy as np
    import re
    from google import genai
    from google.genai import types
    import re, os, time, json, ast
    from dotenv import load_dotenv

    load_dotenv(".env")
    API_KEY = os.getenv("GEMINI_API_KEY")

    client = genai.Client(
		api_key=API_KEY
	)

    df = pd.read_csv(input_csv_path)

    def is_high_index_diagnosa(col):
        match = re.match(r"^result\[(\d+)\]\.", col)
        return match and int(match.group(1)) > 0 

    df = df[[col for col in df.columns if not is_high_index_diagnosa(col)]]

    patterns = [
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]\.diagnosaa$",
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]$",
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]\.jenisDiagnosa$",
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]\.isCopy$",
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]\.jenisDiagnosa.value$",
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]\.isLoadBtnDiagnosaDokter$",
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]\.diagnosaa.value$",
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]\.type$",
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]\.norecDiagnosa$",
        r"^user_input.",
        r"^profile.",
        r"^dpjpUtama",
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]\.0",
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]\.1",
        r"^result\[(\d+)\]\.emrpasienfk",
        r"^result\[(\d+)\]\.diagnosaDokter\[\d+\]\.no",
        r"^result\[(\d+)\]\.dokterDPJP",
        r"^result\[(\d+)\]\._id",
        r"skor",
        r"riwayatImunisasi",
    ]
    for pattern in patterns:
        if not pattern:
            break
        df = df[[col for col in df.columns if not re.match(pattern, col)]]

    df.info()
    def matching_function(pattern, col):
        match = re.match(pattern, col)
        return match and int(match.group(2))>=3
    patterns2 = [
        r"^result\[(\d+)\]\.diagnosaDokter\[(\d+)\]\.",
        r"^result\[(\d+)\]\.diagnosaDokter(\d+)\[",
        r"^result\[(\d+)\]\.diagnosaDokter\[(\d+)\]\.keterangan$",
        r"^result\[(\d+)\]\.diagnosaDokter\[(\d+)\]\.jenisDiagnosa.label$"
    ]
    for pattern in patterns2:
        if not pattern: break
        df = df[[col for col in df.columns if not matching_function(pattern, col)]]

    df.info()

    unwanted_cols = ["no", "uuid", "flag", "intruksiPPA", "kdprofile", "statusenabled", "diagnosaDokter[2].0.jenisDiagnosa.value", "diagnosaDokter[2].0.jenisDiagnosa.label", "diagnosaDokter[2].0.keterangan", "diagnosaDokter[2].0.diagnosaa.label", "diagnosaDokter[2].0.diagnosaa.value", "diagnosaDokter[2].0.type", "diagnosaDokter[2].1.jenisDiagnosa.label", "diagnosaDokter[2].1.jenisDiagnosa.value", "diagnosaDokter[2].1.keterangan", "diagnosaDokter[2].1.type", "keteranganVerifikasiDPJP", "tenagaMedis", "tglVerifikasi", "tgl", "DGizi","created_at","updated_at","update_count","update_before"]
    def removeby (col, unwanted):
        pattern = r"^result\[(\d+)\]\." + unwanted
        match = re.match(pattern, col)
        return match
    for unwanted in unwanted_cols:
        df = df[[col for col in df.columns if not removeby(col, unwanted)]]
    df.info()

    unwanted_cols = ["nocm","catatan_terbaru", "nocmfk","namapasien","suku","objectjeniskelaminfk","noidentitas","nobpjs","noasuransilain","alamatlengkap","kodepos","notelepon","nohp","namaayah","namaibu","email","agama","pendidikan","pekerjaan","isfoto","filename","isFilterProdukLab","enabledEMRSimrsLama","isclosing","objectagamafk"]
    def removeby (col, unwanted):
        pattern = r"^pasien." + unwanted
        match = re.match(pattern, col)
        return match
    for unwanted in unwanted_cols:
        df = df[[col for col in df.columns if not removeby(col, unwanted)]]
    df.info()

    unwanted_cols = ['norec_apd',"emrpasienfk",'norec_pd','noregistrasi','tglregistrasi','namarekanan','objectruanganfk','tglpulang','objectdepartemenfk','objectpegawaifk','asalrujukan','dokter']
    def removeby (col, unwanted):
        pattern = r"^registrasi." + unwanted
        match = re.match(pattern, col)
        return match
    for unwanted in unwanted_cols:
        df = df[[col for col in df.columns if not removeby(col, unwanted)]]
    df.info()

    unwanted_cols = ['dokterRawatBersama','id','created_at','updated_at','statusenabled','noemr']
    df = df[[col for col in df.columns if col not in unwanted_cols]]
    df.info()

    file_path = 'buang_col.txt'
    columns_to_drop = []
    with open(file_path, 'r') as file:
        for line in file:
            columns_to_drop.append(line.strip()) 
    df.drop(columns=columns_to_drop, errors='ignore', inplace=True)
    df.columns = df.columns.str.replace(r'^result\[0\]\.', '', regex=True)
    df.info()

    df['pasien.jeniskelamin'] = df['pasien.jeniskelamin'].map({
        'Perempuan': 'F',
        'Laki-Laki': 'M'
    })
    cols = ['nadi', 'suhu','pernapasan','SPO2','tinggiBadan', 'beratBadan','tekananDarah']

    for index, row in df.iterrows():
        time.sleep(5)
        print(index)

        row_idx = index
        row = df.iloc[row_idx]

        raw_text = row['O']
        if pd.isna(raw_text) or not isinstance(raw_text, str) or raw_text.strip() == "":
            continue

        prompt_text = f"""
            Ekstrak 'nadi', 'suhu','pernapasan','SPO2','tinggiBadan', 'beratBadan','tekananDarah' dari teks di bawah ini.
            Berikan hasilnya dalam format JSON tanpa tambahan teks atau penjelasan.

            Teks:
            \"{raw_text.strip()}\"
            """

        try:
            model = "gemini-2.0-flash"
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt_text),
                    ],
                ),
            ]
            generate_content_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
            )

            response_text=""
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ): response_text += chunk.text

            print(response_text)

            clean_text = re.sub(r"```json|```", "", response_text).strip()
            xdata = json.loads(clean_text)
            df.at[row_idx, "O_extracted"] = xdata

        except Exception as e:
            print(f"Row {index} - Error processing column :", e)
            df.at[row_idx, "O_extracted"] = None

    def safe_dict(x):
        if isinstance(x, dict):
            return x
        if pd.isna(x):
            return {}
        try:
            return ast.literal_eval(str(x))
        except Exception:
            return {}

    df_parsed = df['O_extracted'].apply(safe_dict).apply(pd.Series)
    df = pd.concat([df, df_parsed], axis=1)

    columns_to_replace = ['nadi', 'suhu', 'pernapasan', 'SPO2', 'tinggiBadan', 'beratBadan', 'tekananDarah']
    for col in columns_to_replace:
        if col in df_parsed.columns:
            df[col] = df_parsed[col]

    for index, row in df.iterrows():
        time.sleep(5)

        row_idx = index
        row = df.iloc[row_idx]
        raw_text = row['S']
        print(index)

        if pd.isna(raw_text) or not isinstance(raw_text, str) or raw_text.strip() == "":
            continue

        prompt_text = f"""
            Ekstrak semua keluhan utama secara eksplisit dari teks berikut.
            - Hanya ekstrak yang jelas disebutkan dalam teks.
            - Gunakan format JSON dengan satu key: "keluhan_utama".
            - Nilai dari "keluhan_utama" adalah array berisi string keluhan.
            - Jika tidak ada keluhan, isi array dengan satu item: "Tidak ada keluhan".
            - Jangan tambahkan teks atau penjelasan di luar JSON.

            Teks:
            \"{raw_text.strip()}\"
            """

        try:
            model = "gemini-2.0-flash"
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt_text),
                    ],
                ),
            ]
            generate_content_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
            )

            response_text=""
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ): response_text += chunk.text

            clean_text = re.sub(r"```json|```", "", response_text).strip()
            xdata = json.loads(clean_text)
            df.at[row_idx, "keluhan_extracted"] = xdata

        except Exception as e:
            print(f"Row {index} - Error processing column :", e)
            df.at[row_idx, "keluhan_extracted"] = None

    df["keluhan_extracted"] = df["keluhan_extracted"].fillna("{'keluhan_utama': ['sakit']}")
    df['pengobatan'] = df['P']
    pattern = r"^Unnamed:"
    df = df[[col for col in df.columns if not re.match(pattern, col)]]
    def extract_keluhan_string(x):
        if pd.isna(x):
            return None
        try:
            parsed = ast.literal_eval(x) if isinstance(x, str) else x
            if isinstance(parsed, dict) and 'keluhan_utama' in parsed:
                return ', '.join(parsed['keluhan_utama'])
        except:
            return None
    df['keluhan_utama_str'] = df['keluhan_extracted'].apply(extract_keluhan_string)
    
    df['beratBadan'] = (
        df['beratBadan']
        .astype(str)
        .str.replace(r'[^0-9.,]', '', regex=True)  
        .str.replace(',', '.', regex=False)       
    )
    df['beratBadan'] = pd.to_numeric(df['beratBadan'], errors='coerce')
    df['tinggiBadan'] = (
        df['tinggiBadan']
        .astype(str)
        .str.replace(r'[^0-9.,]', '', regex=True)
        .str.replace(',', '.', regex=False)
    )
    df['tinggiBadan'] = pd.to_numeric(df['tinggiBadan'], errors='coerce')
    df['tekananDarah'] = (
        df['tekananDarah']
        .astype(str)
        .str.replace("\\", "/", regex=False)       
        .str.replace(r'[^0-9/]', '', regex=True)   
    )
    split_bp = df['tekananDarah'].str.split('/', n=1, expand=True)
    df['tekanan_sistolik'] = pd.to_numeric(split_bp[0], errors='coerce')
    df['tekanan_diastolik'] = pd.to_numeric(split_bp[1], errors='coerce')
    df['suhu'] = (
        df['suhu']
        .astype(str)
        .str.replace(',', '.', regex=False)       
        .str.replace(r'[^0-9.]', '', regex=True)   
    )
    df['suhu'] = pd.to_numeric(df['suhu'], errors='coerce')
    df['nadi'] = (
        df['nadi']
        .astype(str)
        .str.replace(r'[^0-9]', '', regex=True)
    )
    df['nadi'] = pd.to_numeric(df['nadi'], errors='coerce')
    df['pernapasan'] = (
        df['pernapasan']
        .astype(str)
        .str.replace(r'[^0-9]', '', regex=True)
    )
    df['pernapasan'] = pd.to_numeric(df['pernapasan'], errors='coerce')
    df.info()
    pattern = r"^Unnamed:"
    df = df[[col for col in df.columns if not re.match(pattern, col)]]
    df = df.rename(columns={
        'O' : 'detailPemeriksaan',
        'S' : 'detailKeluhan',
        'P'  : 'detailPengobatan',
    })
    df.to_csv(output_csv_path, index=False)
