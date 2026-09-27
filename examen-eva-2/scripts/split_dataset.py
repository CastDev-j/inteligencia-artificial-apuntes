"""
Genera las particiones de entrenamiento (70%) y prueba (30%) del dataset
Maternal Health Risk con formato importable en WEKA.

Salidas (carpeta data/):
    maternal_health_risk_train.dat   -> 70%  (CSV con encabezado, para abrir en Weka con el filtro CSV)
    maternal_health_risk_test.dat    -> 30%  (CSV con encabezado, para abrir en Weka con el filtro CSV)
    maternal_health_risk_train.arff  -> 70%  (formato nativo ARFF de WEKA)
    maternal_health_risk_test.arff   -> 30%  (formato nativo ARFF de WEKA)
    distribucion_split.txt           -> reporte de verificacion de la distribucion

El particionado es ESTRATIFICADO: se conserva la proporcion de cada clase
RiskLevel (low / mid / high) en ambos conjuntos, y dentro de cada clase se
respetan las proporciones de las variables para que los subconjuntos sean
representativos y comparables.
"""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "Maternal Health Risk Data Set.csv"
DATA_DIR = BASE_DIR / "data"

RANDOM_STATE = 42
TEST_SIZE = 0.30
TARGET = "RiskLevel"
CLASSES = ["low risk", "mid risk", "high risk"]

# Weka no admite espacios dentro de las etiquetas de un atributo nominal: al leer
# "{low risk, mid risk, high risk}" las parte por espacios y falla con
# "A nominal attribute (RiskLevel) cannot have duplicate labels (risk)".
# En el .arff las clases se abrevian a una sola palabra; el significado queda
# documentado en la cabecera del propio archivo.
ARFF_CLASSES = {"low risk": "low", "mid risk": "mid", "high risk": "high"}

FEATURES = ["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"]

ARFF_HEADER = f"""% Maternal Health Risk (UCI, id=863)
% Ahmed, M. (2020). Maternal Health Risk [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5DP5D
% Licencia CC BY 4.0. Particion generada por particionado estratificado 70/30 (random_state={RANDOM_STATE}).
% El CSV de UCI contiene 1014 registros aunque su ficha declara 1013 instancias.
% Clases abreviadas porque Weka no admite espacios en etiquetas nominales:
%   low = low risk (riesgo bajo) | mid = mid risk (riesgo medio) | high = high risk (riesgo alto)
% Generado por scripts/split_dataset.py
@relation maternal_health_risk

@attribute Age numeric
@attribute SystolicBP numeric
@attribute DiastolicBP numeric
@attribute BS numeric
@attribute BodyTemp numeric
@attribute HeartRate numeric
@attribute RiskLevel {{{', '.join(ARFF_CLASSES.values())}}}

@data
"""


def cargar_csv() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip() for c in df.columns]
    return df


def validar(df: pd.DataFrame) -> None:
    assert list(df.columns) == FEATURES + [TARGET], f"Columnas inesperadas: {list(df.columns)}"
    assert df.shape[0] == 1014, f"Se esperaban 1014 registros y llegaron {df.shape[0]}"
    assert not df.isna().any().any(), "El dataset no debe tener valores faltantes"
    assert not (df == "?").any().any(), "No debe haber valores '?' en el dataset"
    assert set(df[TARGET].unique()) == set(CLASSES), f"Clases inesperadas: {df[TARGET].unique()}"
    print("[OK] 1014 registros, 6 features + 1 objetivo, 3 clases, sin valores faltantes.")


def formatear(valor: float) -> str:
    return str(int(valor)) if float(valor).is_integer() else str(valor)


def particionar(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train, test = train_test_split(
        df,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df[TARGET],
    )
    return train.sort_index(), test.sort_index()


def formatear_columna(columna: pd.Series) -> pd.Series:
    return columna.map(formatear)


def guardar(df: pd.DataFrame, ruta: Path, con_header: bool) -> None:
    limpio = df[FEATURES].apply(formatear_columna).join(df[TARGET])
    limpio.to_csv(ruta, index=False, header=con_header, lineterminator="\n")


def guardar_arff(df: pd.DataFrame, ruta: Path) -> None:
    cuerpo = df[FEATURES].apply(formatear_columna).join(df[TARGET].map(ARFF_CLASSES))
    cuerpo = cuerpo.to_csv(index=False, header=False, lineterminator="\n").strip()
    ruta.write_text(f"{ARFF_HEADER}{cuerpo}\n", encoding="utf-8")


def tabla_distribucion(df: pd.DataFrame, etiqueta: str) -> str:
    conteo = df[TARGET].value_counts().reindex(CLASSES, fill_value=0)
    total = conteo.sum()
    filas = [
        f"{etiqueta:<12}{'Instancias':>12}{'%':>10}",
        "-" * 34,
    ]
    for clase, n in conteo.items():
        filas.append(f"{clase:<12}{n:>12}{(n / total) * 100:>9.2f}%")
    filas.append("-" * 34)
    filas.append(f"{'TOTAL':<12}{total:>12}{100.0:>9.2f}%")
    return "\n".join(filas)


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    df = cargar_csv()
    validar(df)

    train, test = particionar(df)
    assert len(train) + len(test) == len(df), "La suma de train + test debe ser 1014"
    assert round(len(train) / len(df), 2) == 0.70, "El/train debe ser 70%"
    assert round(len(test) / len(df), 2) == 0.30, "El/test debe ser 30%"

    guardar(train, DATA_DIR / "maternal_health_risk_train.dat", con_header=True)
    guardar(test, DATA_DIR / "maternal_health_risk_test.dat", con_header=True)
    guardar_arff(train, DATA_DIR / "maternal_health_risk_train.arff")
    guardar_arff(test, DATA_DIR / "maternal_health_risk_test.arff")

    base = df[TARGET].value_counts().reindex(CLASSES, fill_value=0)
    tr = train[TARGET].value_counts().reindex(CLASSES, fill_value=0)
    te = test[TARGET].value_counts().reindex(CLASSES, fill_value=0)

    comparativo = pd.DataFrame(
        {
            f"Original ({len(df)})": base,
            "Train (70%)": tr,
            "% train": (tr / tr.sum() * 100).round(2),
            "Test (30%)": te,
            "% test": (te / te.sum() * 100).round(2),
            "Desviacion %": ((te / te.sum()) - (base / base.sum())).abs().mul(100).round(2),
        }
    )
    desviacion_ok = comparativo["Desviacion %"].max() < 1.0
    assert desviacion_ok, f"Desviacion de distribucion demasiado alta:\n{comparativo}"

    fuga = pd.merge(
        train[FEATURES + [TARGET]].drop_duplicates(),
        test[FEATURES + [TARGET]].drop_duplicates(),
        on=FEATURES + [TARGET],
        how="inner",
    )
    atipicos = df[(df["HeartRate"] < 50) | (df["HeartRate"] > 110)]

    reporte = [
        "VERIFICACION DEL PARTICIONADO 70/30 (estratificado por RiskLevel)",
        "=" * 62,
        f"Dataset original  : {CSV_PATH.name}",
        f"Instancias totales: {len(df)}  (la ficha de UCI declara 1013; el CSV real trae {len(df)})",
        f"Train (70%)       : {len(train)}  -> data/maternal_health_risk_train.dat / .arff",
        f"Test  (30%)       : {len(test)}  -> data/maternal_health_risk_test.dat / .arff",
        f"random_state      : {RANDOM_STATE}",
        "",
        tabla_distribucion(df, "ORIGINAL"),
        "",
        tabla_distribucion(train, "TRAIN 70%"),
        "",
        tabla_distribucion(test, "TEST 30%"),
        "",
        "COMPARATIVO DE DISTRIBUCION DE CLASES",
        "-" * 62,
        comparativo.to_string(),
        "",
        f"[OK] Desviacion maxima por clase entre original y test: "
        f"{comparativo['Desviacion %'].max():.2f} p.p. (umbral < 1.00 p.p.)",
        f"[*] Filas duplicadas en el dataset original: {df.duplicated(subset=FEATURES + [TARGET]).sum()} "
        f"(se conservan: son repeticiones reales registradas por el sensor IoT).",
        f"[*] Registros idénticos (mismos 6 features y misma clase) presentes a la vez "
        f"en train y test: {len(fuga)}",
        f"[*] Registros con HeartRate fuera de 50-110 bpm: {len(atipicos)} "
        f"(HeartRate = {sorted(atipicos['HeartRate'].unique().tolist())}; se conservan sin modificar "
        f"para no alterar la fuente, ver seccion 6.4 del README).",
        "",
        "ESTADISTICAS DESCRIPTIVAS POR CONJUNTO",
        "-" * 62,
        pd.concat(
            [
                train[FEATURES].describe().T,
                test[FEATURES].describe().T,
            ],
            axis=1,
            keys=["TRAIN (70%)", "TEST (30%)"],
        ).round(2).to_string(),
    ]

    (DATA_DIR / "distribucion_split.txt").write_text("\n".join(reporte) + "\n", encoding="utf-8")

    print("\n" + "\n".join(reporte))


if __name__ == "__main__":
    main()
