import argparse
import asyncio
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import edge_tts  # pip install edge-tts


# =========================
# CONFIG GENERAL
# =========================
ASSETS_DIRNAME = "assets"

# Estructura propuesta (mantiene tus prefijos)
# assets/imagesp/<topic>/<pack>/<key>.png
# assets/audio/<topic>/<pack>/<key>_l1.mp3
# assets/audio/<topic>/<pack>/<key>_l2.mp3
# assets/audio/<topic>/<pack>/<key>_l3.mp3

DEFAULT_VOICE = "en-US-JennyNeural"  # puedes cambiarla
DEFAULT_RATE = "+0%"                 # ejemplo: "-10%" más lento


@dataclass(frozen=True)
class CardItem:
    key: str          # nombre de archivo (sin espacios)
    spoken: str       # texto a pronunciar (puede tener espacios)
    kind: str = "noun"  # noun|country|feeling|number|day|month|etc


@dataclass(frozen=True)
class Pack:
    topic: str
    pack_id: str
    items: List[CardItem]


# =========================
# CURRICULUM A1–A2 (24 temas x 10 items)
# Edita aquí cuando quieras
# =========================
CURRICULUM: List[Pack] = [
    Pack("animals", "pack01", [
        CardItem("cat", "cat"), CardItem("parrot", "parrot"), CardItem("dolphin", "dolphin"),
        CardItem("panda", "panda"), CardItem("turtle", "turtle"), CardItem("hummingbird", "hummingbird"),
        CardItem("rabbit", "rabbit"), CardItem("duck", "duck"), CardItem("eagle", "eagle"),
        CardItem("leopard", "leopard"),
    ]),

    Pack("food_drink", "pack01", [
        CardItem("apple", "apple"), CardItem("banana", "banana"), CardItem("bread", "bread"),
        CardItem("milk", "milk"), CardItem("water", "water"), CardItem("coffee", "coffee"),
        CardItem("tea", "tea"), CardItem("pizza", "pizza"), CardItem("chicken", "chicken"),
        CardItem("rice", "rice"),
    ]),

    Pack("house_home", "pack01", [
        CardItem("bed", "bed"), CardItem("chair", "chair"), CardItem("table", "table"),
        CardItem("sofa", "sofa"), CardItem("kitchen", "kitchen"), CardItem("bathroom", "bathroom"),
        CardItem("door", "door"), CardItem("window", "window"), CardItem("lamp", "lamp"),
        CardItem("fridge", "fridge"),
    ]),

    Pack("family_friends", "pack01", [
        CardItem("mother", "mother"), CardItem("father", "father"), CardItem("sister", "sister"),
        CardItem("brother", "brother"), CardItem("friend", "friend"), CardItem("grandma", "grandma"),
        CardItem("grandpa", "grandpa"), CardItem("aunt", "aunt"), CardItem("uncle", "uncle"),
        CardItem("cousin", "cousin"),
    ]),

    Pack("clothes_Colors", "pack01", [
        CardItem("shirt", "shirt"), CardItem("pants", "pants"), CardItem("dress", "dress"),
        CardItem("shoes", "shoes"), CardItem("hat", "hat"), CardItem("jacket", "jacket"),
        CardItem("socks", "socks"), CardItem("skirt", "skirt"), CardItem("red", "red", "color"),
        CardItem("blue", "blue", "color"),
    ]),

    Pack("numbers_1_10", "pack01", [
        CardItem("one", "one", "number"), CardItem("two", "two", "number"), CardItem("three", "three", "number"),
        CardItem("four", "four", "number"), CardItem("five", "five", "number"), CardItem("six", "six", "number"),
        CardItem("seven", "seven", "number"), CardItem("eight", "eight", "number"),
        CardItem("nine", "nine", "number"), CardItem("ten", "ten", "number"),
    ]),

    Pack("days_months", "pack01", [
        CardItem("monday", "Monday", "day"), CardItem("tuesday", "Tuesday", "day"),
        CardItem("wednesday", "Wednesday", "day"), CardItem("thursday", "Thursday", "day"),
        CardItem("friday", "Friday", "day"), CardItem("saturday", "Saturday", "day"),
        CardItem("sunday", "Sunday", "day"),
        CardItem("january", "January", "month"), CardItem("february", "February", "month"),
        CardItem("march", "March", "month"),
    ]),

    Pack("feelings", "pack01", [
        CardItem("happy", "happy", "feeling"), CardItem("sad", "sad", "feeling"),
        CardItem("tired", "tired", "feeling"), CardItem("hungry", "hungry", "feeling"),
        CardItem("thirsty", "thirsty", "feeling"), CardItem("angry", "angry", "feeling"),
        CardItem("scared", "scared", "feeling"), CardItem("cold", "cold", "feeling"),
        CardItem("hot", "hot", "feeling"), CardItem("okay", "okay", "feeling"),
    ]),

    Pack("tech_communication", "pack01", [
        CardItem("phone", "phone"), CardItem("computer", "computer"), CardItem("tablet", "tablet"),
        CardItem("tv", "TV"), CardItem("radio", "radio"), CardItem("camera", "camera"),
        CardItem("internet", "internet"), CardItem("email", "email"), CardItem("message", "message"),
        CardItem("call", "call"),
    ]),

    Pack("body", "pack01", [
        CardItem("head", "head"), CardItem("eyes", "eyes"), CardItem("ears", "ears"),
        CardItem("mouth", "mouth"), CardItem("nose", "nose"), CardItem("hand", "hand"),
        CardItem("arm", "arm"), CardItem("leg", "leg"), CardItem("foot", "foot"),
        CardItem("stomach", "stomach"),
    ]),

    Pack("health", "pack01", [
        CardItem("doctor", "doctor"), CardItem("nurse", "nurse"), CardItem("medicine", "medicine"),
        CardItem("pain", "pain"), CardItem("fever", "fever"), CardItem("cough", "cough"),
        CardItem("hospital", "hospital"), CardItem("pharmacy", "pharmacy"),
        CardItem("appointment", "appointment"), CardItem("emergency", "emergency"),
    ]),

    Pack("buildings", "pack01", [
        CardItem("bank", "bank"), CardItem("school", "school"), CardItem("hospital", "hospital"),
        CardItem("library", "library"), CardItem("supermarket", "supermarket"),
        CardItem("restaurant", "restaurant"), CardItem("hotel", "hotel"),
        CardItem("airport", "airport"), CardItem("station", "station"),
        CardItem("police_station", "police station"),
    ]),

    Pack("town_places", "pack01", [
        CardItem("street", "street"), CardItem("park", "park"), CardItem("market", "market"),
        CardItem("museum", "museum"), CardItem("cinema", "cinema"), CardItem("church", "church"),
        CardItem("beach", "beach"), CardItem("mountain", "mountain"),
        CardItem("river", "river"), CardItem("bridge", "bridge"),
    ]),

    Pack("transport", "pack01", [
        CardItem("car", "car"), CardItem("bus", "bus"), CardItem("train", "train"),
        CardItem("subway", "subway"), CardItem("taxi", "taxi"), CardItem("bicycle", "bicycle"),
        CardItem("airplane", "airplane"), CardItem("boat", "boat"),
        CardItem("ticket", "ticket"), CardItem("map", "map"),
    ]),

    Pack("shopping_money", "pack01", [
        CardItem("money", "money"), CardItem("dollar", "dollar"), CardItem("price", "price"),
        CardItem("cheap", "cheap"), CardItem("expensive", "expensive"), CardItem("buy", "buy"),
        CardItem("sell", "sell"), CardItem("receipt", "receipt"),
        CardItem("credit_card", "credit card"), CardItem("cash", "cash"),
    ]),

    Pack("documents_texts", "pack01", [
        CardItem("form", "form"), CardItem("passport", "passport"), CardItem("id_card", "ID card"),
        CardItem("menu", "menu"), CardItem("sign", "sign"), CardItem("letter", "letter"),
        CardItem("email", "email"), CardItem("message", "message"),
        CardItem("ticket", "ticket"), CardItem("map", "map"),
    ]),

    Pack("education", "pack01", [
        CardItem("teacher", "teacher"), CardItem("student", "student"), CardItem("classroom", "classroom"),
        CardItem("homework", "homework"), CardItem("book", "book"), CardItem("pen", "pen"),
        CardItem("pencil", "pencil"), CardItem("notebook", "notebook"),
        CardItem("exam", "exam"), CardItem("lesson", "lesson"),
    ]),

    Pack("work", "pack01", [
        CardItem("job", "job"), CardItem("office", "office"), CardItem("meeting", "meeting"),
        CardItem("boss", "boss"), CardItem("colleague", "colleague"), CardItem("salary", "salary"),
        CardItem("schedule", "schedule"), CardItem("computer", "computer"),
        CardItem("break", "break"), CardItem("email", "email"),
    ]),

    Pack("hobbies", "pack01", [
        CardItem("music", "music"), CardItem("reading", "reading"), CardItem("cooking", "cooking"),
        CardItem("dancing", "dancing"), CardItem("drawing", "drawing"), CardItem("gardening", "gardening"),
        CardItem("travel", "travel"), CardItem("games", "games"),
        CardItem("photography", "photography"), CardItem("swimming", "swimming"),
    ]),

    Pack("sports", "pack01", [
        CardItem("soccer", "soccer"), CardItem("basketball", "basketball"), CardItem("tennis", "tennis"),
        CardItem("baseball", "baseball"), CardItem("running", "running"), CardItem("cycling", "cycling"),
        CardItem("swimming", "swimming"), CardItem("yoga", "yoga"),
        CardItem("gym", "gym"), CardItem("golf", "golf"),
    ]),

    Pack("weather_seasons", "pack01", [
        CardItem("sunny", "sunny"), CardItem("rainy", "rainy"), CardItem("cloudy", "cloudy"),
        CardItem("windy", "windy"), CardItem("snowy", "snowy"), CardItem("hot", "hot"),
        CardItem("cold", "cold"), CardItem("spring", "spring", "season"),
        CardItem("summer", "summer", "season"), CardItem("winter", "winter", "season"),
    ]),

    Pack("countries", "pack01", [
        CardItem("united_states", "United States", "country"),
        CardItem("canada", "Canada", "country"),
        CardItem("mexico", "Mexico", "country"),
        CardItem("colombia", "Colombia", "country"),
        CardItem("brazil", "Brazil", "country"),
        CardItem("spain", "Spain", "country"),
        CardItem("france", "France", "country"),
        CardItem("china", "China", "country"),
        CardItem("japan", "Japan", "country"),
        CardItem("india", "India", "country"),
    ]),
]


# =========================
# TEMPLATES de frases por nivel
# =========================
VOWELS = set("aeiou")


def a_or_an(word: str) -> str:
    w = word.strip().lower()
    # heurística simple (suficiente para MVP)
    return "an" if w and w[0] in VOWELS else "a"


def level_texts(topic: str, item: CardItem) -> Dict[str, str]:
    """
    Devuelve textos para L1/L2/L3.
    L1: palabra
    L2: frase simple
    L3: frase en contexto (A2)
    """
    spoken = item.spoken

    # L1
    l1 = spoken

    # L2 & L3 por tipo
    if item.kind == "number":
        l2 = spoken
        l3 = f"I can count: {spoken}."
    elif item.kind == "day":
        l2 = f"Today is {spoken}."
        l3 = f"On {spoken}, I study English."
    elif item.kind == "month":
        l2 = f"It is {spoken}."
        l3 = f"In {spoken}, the weather can change."
    elif item.kind == "feeling":
        l2 = f"I am {spoken}."
        l3 = f"Today I feel {spoken}."
    elif item.kind == "country":
        l2 = f"This is {spoken}."
        l3 = f"I am from {spoken}."
    elif item.kind == "season":
        l2 = f"It is {spoken}."
        l3 = f"In {spoken}, I like to go outside."
    elif item.kind == "color":
        l2 = f"This is {spoken}."
        l3 = f"My favorite color is {spoken}."
    else:
        art = a_or_an(spoken)
        l2 = f"This is {art} {spoken}."
        # contexto por tema (muy simple pero útil)
        if topic in {"animals"}:
            l3 = f"The {spoken} is here."
        elif topic in {"food_drink"}:
            l3 = f"I like {spoken}."
        elif topic in {"house_home"}:
            l3 = f"The {spoken} is in the house."
        elif topic in {"family_friends"}:
            l3 = f"This is my {spoken}."
        elif topic in {"transport"}:
            l3 = f"I go by {spoken}."
        else:
            l3 = f"I see {art} {spoken}."

    return {"l1": l1, "l2": l2, "l3": l3}


# =========================
# UTILIDADES
# =========================
def ensure_ffmpeg() -> None:
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception:
        raise RuntimeError(
            "No encontré 'ffmpeg' en tu PATH. Instálalo y reinicia la terminal. "
            "Luego prueba: ffmpeg -version"
        )


def ffmpeg_wav_to_mp3(wav_path: Path, mp3_path: Path) -> None:
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-i", str(wav_path),
        "-ac", "1",
        "-ar", "22050",
        "-b:a", "64k",
        str(mp3_path),
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


async def tts_to_mp3(text: str, mp3_path: Path, voice: str, rate: str) -> None:
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(str(mp3_path))


async def bounded_gather(coros, limit: int = 3):
    sem = asyncio.Semaphore(limit)

    async def _run(c):
        async with sem:
            return await c

    return await asyncio.gather(*[_run(c) for c in coros])


def write_content_index(assets_dir: Path, packs: List[Pack]) -> None:
    """
    Crea un índice JSON para tu app (te servirá para la siguiente fase).
    """
    out = {
        "version": 1,
        "packs": []
    }
    for p in packs:
        pack_obj = {
            "topic": p.topic,
            "pack_id": p.pack_id,
            "cards": []
        }
        for it in p.items:
            texts = level_texts(p.topic, it)
            card = {
                "key": it.key,
                "spoken": it.spoken,
                "image": f"imagesp/{p.topic}/{p.pack_id}/{it.key}.png",
                "audio_l1": f"audio/{p.topic}/{p.pack_id}/{it.key}_l1.mp3",
                "audio_l2": f"audio/{p.topic}/{p.pack_id}/{it.key}_l2.mp3",
                "audio_l3": f"audio/{p.topic}/{p.pack_id}/{it.key}_l3.mp3",
                "text_l1": texts["l1"],
                "text_l2": texts["l2"],
                "text_l3": texts["l3"],
            }
            pack_obj["cards"].append(card)
        out["packs"].append(pack_obj)

    index_path = assets_dir / "content_index.json"
    index_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")


def create_dirs(assets_dir: Path, packs: List[Pack]) -> None:
    for p in packs:
        (assets_dir / "audio" / p.topic / p.pack_id).mkdir(parents=True, exist_ok=True)
        (assets_dir / "imagesp" / p.topic / p.pack_id).mkdir(parents=True, exist_ok=True)
        # Archivo marcador para que git no ignore carpetas vacías (opcional)
        keep = assets_dir / "imagesp" / p.topic / p.pack_id / ".keep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")


def copy_existing_top_level_images_into_animals_pack(assets_dir: Path) -> None:
    """
    Copia tus PNG actuales (assets/imagesp/*.png) a assets/imagesp/animals/pack01/
    SIN borrarlos del lugar original (para no romper tu prototipo).
    """
    src_dir = assets_dir / "imagesp"
    dst_dir = assets_dir / "imagesp" / "animals" / "pack01"
    dst_dir.mkdir(parents=True, exist_ok=True)

    for png in src_dir.glob("*.png"):
        target = dst_dir / png.name
        if not target.exists():
            shutil.copy2(png, target)


def convert_existing_wavs(assets_dir: Path, overwrite: bool) -> None:
    """
    Convierte WAV existentes bajo assets/audio/*.wav a mp3 en assets/audio/animals/pack01/<name>_l2.mp3
    (asumimos que tu WAV actual corresponde a la frase principal - nivel 2).
    """
    ensure_ffmpeg()
    src_dir = assets_dir / "audio"
    dst_dir = assets_dir / "audio" / "animals" / "pack01"
    dst_dir.mkdir(parents=True, exist_ok=True)

    for wav in src_dir.glob("*.wav"):
        name = wav.stem  # cat, parrot, etc.
        out_mp3 = dst_dir / f"{name}_l2.mp3"
        if out_mp3.exists() and not overwrite:
            continue
        ffmpeg_wav_to_mp3(wav, out_mp3)


async def generate_all_tts_mp3(assets_dir: Path, packs: List[Pack], voice: str, rate: str,
                               overwrite: bool, concurrency: int) -> None:
    tasks = []

    for p in packs:
        for it in p.items:
            texts = level_texts(p.topic, it)

            out_l1 = assets_dir / "audio" / p.topic / p.pack_id / f"{it.key}_l1.mp3"
            out_l2 = assets_dir / "audio" / p.topic / p.pack_id / f"{it.key}_l2.mp3"
            out_l3 = assets_dir / "audio" / p.topic / p.pack_id / f"{it.key}_l3.mp3"

            # Si ya existe, se salta (a menos que overwrite)
            if overwrite or not out_l1.exists():
                tasks.append(tts_to_mp3(texts["l1"], out_l1, voice, rate))
            if overwrite or not out_l2.exists():
                tasks.append(tts_to_mp3(texts["l2"], out_l2, voice, rate))
            if overwrite or not out_l3.exists():
                tasks.append(tts_to_mp3(texts["l3"], out_l3, voice, rate))

    # Ejecutar con límite de concurrencia para no saturar
    await bounded_gather(tasks, limit=concurrency)


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", default=ASSETS_DIRNAME, help="Ruta a la carpeta assets/")
    ap.add_argument("--voice", default=DEFAULT_VOICE, help="Voz edge-tts (ej: en-US-JennyNeural)")
    ap.add_argument("--rate", default=DEFAULT_RATE, help="Rate edge-tts (ej: -10%%, +0%%)")
    ap.add_argument("--overwrite", action="store_true", help="Sobrescribir MP3 existentes")
    ap.add_argument("--concurrency", type=int, default=3, help="Concurrencia TTS (1-5 recomendado)")
    ap.add_argument("--convert-wavs", action="store_true", help="Convertir WAV existentes a MP3 (nivel2)")
    ap.add_argument("--copy-images", action="store_true", help="Copiar PNG top-level a animals/pack01")
    return ap.parse_args()


async def main():
    args = parse_args()
    assets_dir = Path(args.assets).resolve()

    if not assets_dir.exists():
        raise FileNotFoundError(f"No existe assets dir: {assets_dir}")

    # 1) Crear estructura completa
    create_dirs(assets_dir, CURRICULUM)

    # 2) Crear índice JSON (siguiente fase: cargar packs desde JSON)
    write_content_index(assets_dir, CURRICULUM)

    # 3) Convertir WAV existentes (si pides)
    if args.convert_wavs:
        convert_existing_wavs(assets_dir, overwrite=args.overwrite)

    # 4) Copiar PNG actuales (si pides)
    if args.copy_images:
        copy_existing_top_level_images_into_animals_pack(assets_dir)

    # 5) Generar MP3 con TTS (L1/L2/L3) para TODO
    await generate_all_tts_mp3(
        assets_dir=assets_dir,
        packs=CURRICULUM,
        voice=args.voice,
        rate=args.rate,
        overwrite=args.overwrite,
        concurrency=max(1, min(args.concurrency, 8)),
    )

    print("✅ Listo. Estructura creada y MP3 generados.")
    print(f"📁 Revisa: {assets_dir / 'audio'}")
    print(f"📁 Revisa: {assets_dir / 'imagesp'}")
    print(f"🧾 Índice: {assets_dir / 'content_index.json'}")


if __name__ == "__main__":
    asyncio.run(main())
