
def process_resumemedis_data(input_csv_path, output_csv_path):
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

    
    patterns = [
        r"^diagnosaDokter\[\d+\]\.no$",
        r"^diagnosaDokter\[\d+\]\.jenisDiagnosa.value$",
        r"^diagnosaDokter\[\d+\]\.jenisDiagnosa.label$",
        r"^detailTindakan\[\d+\]\.no$",
        r"^diagnosaDokter\[\d+\]\.norecDiagnosa$",
        r"^detailTindakan\[\d+\]\.norecDiagnosa",
        r"^detailObatResep\[\d+\]\.waktupakai",
        r"^detailObatResep\[\d+\]\.no",
        r"^detailObatResep\[\d+\]\.obat.label$",
        r"^detailObatResep\[\d+\]\.obat.value$",
        r"^detailObatResep\[\d+\]\.jumlah$",
        r"^detailObatResep\[\d+\]\.aturanPakai$",
        r"^detailObatResep\[\d+\]\.waktuPakai$",
        r"^detailObatResep\[\d+\]\.dosis$",
        r"^detailDokterPelayanan",
        r"^dokterDPJP",
        r"^diagnosaDokter\[(\d+)\]\.isLoadBtnDiagnosaDokter$",
        r"^diagnosaDokter\[(\d+)\]\.jenisDiagnosa$",
        r"^detailObatResep\[(\d+)\]\.obat$",
        r"^detailObatResep\[(\d+)\]\.jenisObat$",
        r"^diagnosaDokter\[(\d+)\]\.diagnosaIcd10$",
        r"^detailTindakan\[(\d+)\]\.diagnosaIcd9$",
        r"^detailTindakan\[(\d+)\]\.diagnosaIcd9.value$",
        r"^diagnosaDokter\[(\d+)\]\.diagnosaIcd10.value$",
        r"^detailTindakan\[(\d+)\]\.diagnosaIcd9.value$",
        r"^detailTindakan\[(\d+)\]\.diagnosaIcd9$",
        ]
    for pattern in patterns:
        df = df[[col for col in df.columns if not re.match(pattern, col)]]

    def matching_function(pattern, col):
        match = re.match(pattern, col)
        return match and int(match.group(1))>=3

    patterns2 = [
        r"^detailTindakan\[(\d+)\]\.diagnosaIcd9.label$",
        r"^diagnosaDokter\[(\d+)\]\.ketDiagnosaDok$",
        r"^diagnosaDokter\[(\d+)\]\.diagnosaIcd10.label$",
        r"^detailTindakan\[(\d+)\]\.ketTindakanDokter$",
        r"^detailTindakan\[(\d+)\]\.diagnosaIcd9$",
    ]
    for pattern in patterns2:
        df = df[[col for col in df.columns if not matching_function(pattern, col)]]

    df.info()

    unwanted_cols = ["no","poli","pasien.catatan_terbaru","dokterDPJP","pasien.namapasien", "skalaNyeri", "pasien.tempatlahir", "pasien.suku","pasien.objectjeniskelaminfk", "hasilKonsultasi","diet", "flag", "instruksiPPA", "kdprofile", "statusenabled", "diagnosaDokter[2].0.jenisDiagnosa.value", "diagnosaDokter[2].0.jenisDiagnosa.label", "diagnosaDokter[2].0.keterangan", "diagnosaDokter[2].0.diagnosaa.label", "diagnosaDokter[2].0.diagnosaa.value", "diagnosaDokter[2].0.type", "diagnosaDokter[2].1.jenisDiagnosa.label", "diagnosaDokter[2].1.jenisDiagnosa.value", "diagnosaDokter[2].1.keterangan", "diagnosaDokter[2].1.type", "keteranganVerifikasiDPJP", "tenagaMedis", "detailDokterPelayanan[0].no","dokterDPJP.label","dokterDPJP.value","pelaksana"]
    unwanted_cols2 = ["pasien.noidentitas","pasien.nocm", "detailTindakan[0].isLoadBtnDiagnosaDokter9", "pasien.nocmfk","pasien.nobpjs", "pasien.noasuransilain","pasien.alamatlengkap","pasien.kodepos","pasien.notelepon","pasien.nohp","pasien.namaayah","pasien.namaibu","pasien.email","pasien.agama","pasien.pendidikan","pasien.pekerjaan","pasien.isfoto","pasien.filename","pasien.catatan","pasien.isFilterProdukLab","pasien.enabledEMRSimrsLama","statusenabled","noemr","emrpasienfk","id","created_at","updated_at","IMT","kondisiKeluar","statusSelesai","totalSkor","alergiReaksiObat","gcs","hasilPenunjang","kesadaran","kondisiKeluarLainya","poli.value","tglperjanjian","pemeriksaanfisiklainnya","statusWA","tidakAdaTurunBeratBadan","turunBeratBadan","asupanMakan","riwayatPenyakitSekarang","alergireaksiobat","hasilkonsultasi","hasilpenunjang","skalaNyeri->label"]
    wanted_cols  = ["registrasi.kelompokpasien", "registrasi.asalrujukan","registrasi.namakelas", "pasien.nocm", "pasien.nocmfk", "pasien.tgllahir", "pasien.jeniskelamin", "pasien.umur"]

    df = df[[col for col in df.columns if col not in unwanted_cols]]
    df = df[[col for col in df.columns if col not in unwanted_cols2]]
    df = df[[col for col in df.columns if not (col.startswith("registrasi") and col not in wanted_cols)]]
    df = df[[col for col in df.columns if not (col.startswith("pasien.") and col not in wanted_cols)]]
    df = df[[col for col in df.columns if not (col.startswith("user_input.") or col.startswith("profile.") or col.startswith("prognosis"))]]

    df.info()

    df['pasien.jeniskelamin'] = df['pasien.jeniskelamin'].map({
        'Perempuan': 'F',
        'Laki-Laki': 'M'
    })

    for index, row in df.iterrows():
        time.sleep(5)

        row_idx = index
        row = df.iloc[row_idx]
        raw_text = row['riwayatPenyakit']
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

    df.to_csv(output_csv_path, index=False)
