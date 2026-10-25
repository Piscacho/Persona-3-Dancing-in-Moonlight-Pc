#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Trophies of Persona 3: Dancing in Moonlight (CUSA12636): the list and the unlocks.

The game unlocks a trophy through sceNpTrophyUnlockTrophy with its id; the runtime appends
"id unix-time" to <user>/trophies.log and shows the notice in game. The names and descriptions
live here because the game's own trophy texts (TROP.ESFM) are encrypted; the icons are read
from sce_sys/trophy/trophy00.trp, where they are plain PNG files (TROP000.PNG = trophy 0).

As a script: trophies.py <game> --out <dir> writes <dir>/trophies.txt (id, grade, name per line,
read by the runtime) and the icons to <dir>/trophies/.
"""
import argparse
from pathlib import Path
import struct

PLATINUM, GOLD, SILVER, BRONZE = 'platinum', 'gold', 'silver', 'bronze'
GRADES = (PLATINUM, GOLD, SILVER, BRONZE)
PLATINUM_ID = 0
LOG_NAME = 'trophies.log'

# (id, grade, name, description)
TROPHIES = [
    (0, PLATINUM, 'Dancing in Moonlight', 'Obtained all trophies.'),
    (1, BRONZE, 'Better Safe than Sorry', 'Played a tutorial.'),
    (2, BRONZE, 'Just Another Day', 'Watched a Social event.'),
    (3, BRONZE, 'The Crib Visit', "Explored a friend's room."),
    (4, BRONZE, "The Leader's Demeanor", 'Watched 20 Social events.'),
    (5, SILVER, 'Best Buds', "Explored all the guys' rooms."),
    (6, SILVER, 'Naturally Popular', "Explored all the girls' rooms."),
    (7, SILVER, 'The Party Never Stops', "Made Elle-P's ball a success."),
    (8, GOLD, "It's Gotta Be You", 'Watched all Social events.'),
    (9, BRONZE, "Searchin' the Premises", "Obtained 5 rewards from Elle-P's card search."),
    (10, SILVER, "Koromaru's Rival", "Obtained all rewards from Elle-P's card search."),
    (11, BRONZE, 'The Selfish Producer', 'Had Elle-P join the ball.'),
    (12, SILVER, 'The Time for Challenge Has Come', 'Unlocked the highest difficulty level (ALL NIGHT).'),
    (13, BRONZE, 'IRL Debut', 'Obtained a costume.'),
    (14, SILVER, "It Won't Fit in my Wardrobe!", 'Obtained half of all the costumes.'),
    (15, GOLD, 'Fashion Monster', 'Obtained all the costumes.'),
    (16, BRONZE, 'The One Who Gathered the Glasses', 'Obtained all the pairs of glasses.'),
    (17, BRONZE, 'Getting the Shiny Things', 'Obtained half of all the accessories.'),
    (18, SILVER, 'The Dancing Jeweler', 'Obtained all of the accessories.'),
    (19, BRONZE, 'If You Would Kindly Excuse Yourself', 'Failed a stage.'),
    (20, BRONZE, 'Welcome to the Club', 'Cleared a stage.'),
    (21, SILVER, 'The Usurper of Rankings', 'Earned the highest possible grade on a stage (KING CRAZY).'),
    (22, SILVER, 'Innate Ability', 'Cleared a stage on HARD or harder and earned a PERFECT rating on at least half of the Notes.'),
    (23, BRONZE, 'Going into Orgia Mode', 'Beat your own high score.'),
    (24, BRONZE, 'Who Even Are You?', 'Started a stage with a different hairstyle, two accessories, colored contacts, and a colored wig.'),
    (25, BRONZE, 'An Exclusive Stylist', 'Changed costumes and played a stage with each of the members of SEES (excluding Koromaru and Shinjiro).'),
    (26, GOLD, 'Full Bloom Fever', 'Watched 40 different Fever Time dances.'),
    (27, SILVER, 'Can\'t Say "I Don\'t Care" Now', 'Watched every possible dance for the P3 Protagonist (Makoto Yuki).'),
    (28, SILVER, 'The Dancing Anti-Shadow Weapon', 'Watched every possible dance for Aigis.'),
    (29, BRONZE, 'The Veteran Pair', 'Cleared the stages where Akihiko and Mitsuru dance together.'),
    (30, BRONZE, 'The Dependable Classmates', 'Cleared the stages where Yukari and Junpei dance together.'),
    (31, BRONZE, 'The Difficulty of Communication', 'Cleared the stages where Fuuka and Ken dance together.'),
    (32, BRONZE, "Let's Do It Again!", 'Watched a replay.'),
    (33, BRONZE, "I Couldn't Help It...", 'Unlocked all ???s in Collection.'),
    (34, BRONZE, 'Personalized Fashion', 'Registered a costume as a Favorite.'),
    (35, SILVER, 'Down to the Bone', 'Unlocked all Custom modifiers.'),
    (36, BRONZE, "As Long As You're Groovin'", 'Cleared a stage after changing Hype Gauge difficulty in Custom.'),
    (37, BRONZE, 'Carrot and Stick Approach', 'Cleared a stage with both "GOOD ratings won\'t break combos" and "Game Over with combo break" enabled.'),
    (38, BRONZE, 'The Unhittable Pitch', 'Cleared a stage with both "Note paths waver" and "Note speed fluctuates" enabled.'),
    (39, BRONZE, 'Committed to the Result', 'Cleared a stage on HARD or harder with all Support modifiers enabled.'),
    (40, BRONZE, 'Unstoppable Force, Immovable Object', 'Cleared a stage with 5 Challenge and 5 Support modifiers simultaneously enabled.'),
    (41, BRONZE, 'Chance Encounter with the Final Boss', 'Started a stage on ALL NIGHT difficulty with 10 or more Challenge modifiers enabled.'),
]
BY_ID = {t[0]: t for t in TROPHIES}
# Spanish: id -> (name, description).
SPANISH = {
    0: ('Dancing in Moonlight', 'Consigue el resto de trofeos del juego.'),
    1: ('Más vale prevenir que curar', 'Juega un tutorial.'),
    2: ('Un día más', 'Ve un evento social.'),
    3: ('La visita a la choza', 'Explora la habitación de un amigo.'),
    4: ('La conducta del capitán', 'Ve 20 eventos sociales.'),
    5: ('Grandes colegas', 'Explora las habitaciones de todos los chicos.'),
    6: ('Popular por naturaleza', 'Explora las habitaciones de todas las chicas.'),
    7: ('Que no pare la fiesta', 'Consigue que el baile de Elle-P sea un éxito.'),
    8: ('Tienes que ser tú', 'Ve todos los eventos sociales.'),
    9: ('Búsqueda en las instalaciones', 'Consigue 5 recompensas de la búsqueda de cartas de Elle-P.'),
    10: ('Rival de Koromaru', 'Consigue todas las recompensas de la búsqueda de cartas de Elle-P.'),
    11: ('La productora egoísta', 'Consigue que Elle-P se una al baile.'),
    12: ('Ha llegado la hora del desafío', 'Desbloquea la mayor dificultad (ALL NIGHT).'),
    13: ('Debut en la vida real', 'Consigue un atuendo.'),
    14: ('¡No me cabe en el armario!', 'Consigue la mitad de los atuendos.'),
    15: ('As de la moda', 'Consigue todos los atuendos.'),
    16: ('Aquel que reunió todas las gafas', 'Consigue todos los pares de gafas.'),
    17: ('Si brilla, es mío', 'Consigue la mitad de los accesorios.'),
    18: ('El bailarín joyero', 'Consigue todos los accesorios.'),
    19: ('Si es tan amable de disculparme', 'No superes una fase.'),
    20: ('Bienvenido al club', 'Supera una fase.'),
    21: ('El usurpador de clasificaciones', 'Consigue el mayor grado posible en una fase (KING CRAZY).'),
    22: ('Habilidad innata', 'Completa una fase en HARD o superior y consigue una puntuación PERFECT en al menos la mitad de las notas.'),
    23: ('Modo orgía activado', 'Supera tu mejor puntuación.'),
    24: ('¿Pero tú quién eres?', 'Empieza una fase con un peinado diferente, dos accesorios, lentillas de colores y una peluca de colores.'),
    25: ('Un estilista exclusivo', 'Cambia de atuendo y juega una fase con cada uno de los miembros del SEES (sin incluir a Koromaru y Shinjiro).'),
    26: ('Fiebre álgida', 'Entra en Fiebre en 40 bailes distintos.'),
    27: ('Ya no puedo decir que no me importa', 'Ve todos los bailes posibles para el protagonista de P3 (Makoto Yuki).'),
    28: ('El arma anti-Sombras bailarina', 'Ve todos los bailes posibles para Aigis.'),
    29: ('La pareja veterana', 'Completa las fases en las que Akihiko y Mitsuru bailan juntos.'),
    30: ('Los compañeros de clase fiables', 'Completa las fases en las que Yukari y Junpei bailan juntos.'),
    31: ('La dificultad de la comunicación', 'Completa las fases en las que Fuuka y Ken bailan juntos.'),
    32: ('¡Vamos, otra vez!', 'Ve una repetición.'),
    33: ('No he podido evitarlo...', 'Desbloquea todos los ??? en Collection.'),
    34: ('Moda personalizada', 'Registra un atuendo como favorito.'),
    35: ('Hasta la médula', 'Desbloquea todos los modificadores en Personalizado.'),
    36: ('Mientras muevas el esqueleto...', 'Completa una fase tras cambiar la dificultad del medidor de Furor en Personalizado.'),
    37: ('El método de la zanahoria y el palo', 'Completa una fase con las opciones "GOOD no interrumpe los combos" y "Fin de la partida al interrumpir un combo" habilitadas.'),
    38: ('El tono inalcanzable', 'Completa una fase con las opciones "La ruta de las notas se mueve" y "La velocidad de las notas varía durante el tema" habilitadas.'),
    39: ('Comprometido con el resultado', 'Completa una fase en HARD o superior con todos los modificadores de Ayuda habilitados.'),
    40: ('Fuerza imparable, objeto inamovible', 'Completa una fase con 5 modificadores de Desafío y 5 de Ayuda habilitados simultáneamente.'),
    41: ('Encuentro fortuito con el jefe final', 'Empieza una fase en dificultad ALL NIGHT con 10 o más modificadores de Desafío habilitados.'),
}
TRANSLATIONS = {'es': SPANISH}


def text(trophy, language=None):
    """(name, description) of a trophy in `language` ('es', ...) when there is a translation,
    else in English."""
    _id, _grade, name, description = BY_ID[trophy]
    local = TRANSLATIONS.get((language or '')[:2], {}).get(trophy)
    if local:
        return local[0] or name, local[1] or description
    return name, description


def read_log(path):
    """{id: earliest unlock time} from a trophies.log; broken lines are skipped."""
    unlocked = {}
    try:
        text = Path(path).read_text(encoding='utf-8', errors='replace')
    except OSError:
        return unlocked
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            trophy, when = int(parts[0]), int(parts[1])
            if trophy in BY_ID and (trophy not in unlocked or when < unlocked[trophy]):
                unlocked[trophy] = when
    return unlocked


def trp_files(path):
    """{name: bytes} of the unencrypted entries (the PNG icons) of a trophy00.trp."""
    data = Path(path).read_bytes()
    magic, _version, _size, count, entry_size = struct.unpack_from('>IIQII', data, 0)
    if magic != 0xDCA24D00 or entry_size < 52:
        raise ValueError('not a trophy file')
    files = {}
    for i in range(count):
        at = 0x60 + i * entry_size
        name = data[at:at + 32].split(b'\0')[0].decode('ascii', 'replace')
        offset, size, flags = struct.unpack_from('>QQI', data, at + 32)
        blob = data[offset:offset + size]
        if blob[:4] == b'\x89PNG':
            files[name] = blob
    return files


def icon_name(trophy):
    return f'TROP{trophy:03d}.PNG'


def prepare(game, out, language=None):
    """trophies.txt for the runtime (names in `language` when translated) and the icons, from the
    game's trophy file when it has one."""
    out = Path(out)
    folder = out / 'trophies'
    folder.mkdir(parents=True, exist_ok=True)
    icons = 0
    trp = Path(game) / 'sce_sys' / 'trophy' / 'trophy00.trp'
    try:
        for name, blob in trp_files(trp).items():
            target = folder / name
            if not target.is_file() or target.stat().st_size != len(blob):
                target.write_bytes(blob)
            icons += name.startswith('TROP')
    except (OSError, ValueError, struct.error) as error:
        print(f'Trophies: no icons ({error})')
    lines = [f'{trophy}\t{grade}\t{text(trophy, language)[0]}' for trophy, grade, _name, _text in TROPHIES]
    (out / 'trophies.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Trophies: {len(TROPHIES)} known, {icons} icons')
    return out / 'trophies.txt', folder


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('game', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--language', default=None)
    args = parser.parse_args()
    prepare(args.game, args.out, args.language)
