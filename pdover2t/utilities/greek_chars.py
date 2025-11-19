"""

https://docs.python.org/3/library/unicodedata.html
https://www.unicode.org/Public/UCD/latest/ucd/NamesList.txt
https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals
https://realpython.com/python-encodings-guide/#python-string-literals-ways-to-skin-a-cat
"""
greek_letters_map = {
    'Alpha': 'Α',
    'Beta': 'Β',
    'Chi': 'Χ',
    'Delta': 'Δ',             # "\N{GREEK CAPITAL LETTER DELTA}"
    'Epsilon': 'Ε',
    'Eta': 'Η',
    'Gamma': 'Γ',
    'Iota': 'Ι',
    'Kappa': 'Κ',
    'Lamda': 'Λ',
    'Mu': 'Μ',
    'Nu': 'Ν',
    'Omega': 'Ω',
    'Omicron': 'Ο',
    'Phi': 'Φ',
    'Pi': 'Π',
    'Psi': 'Ψ',
    'Rho': 'Ρ',
    'Sigma': 'Σ',
    'Tau': 'Τ',
    'Theta': 'Θ',
    'Upsilon': 'Υ',
    'Xi': 'Ξ',
    'Zeta': 'Ζ',
    'alpha': 'α',
    'beta': 'β',
    'chi': 'χ',
    'delta': 'δ',    # "\N{GREEK SMALL LETTER DELTA}"
    'epsilon': 'ε',
    'eta': 'η',
    'gamma': 'γ',
    'iota': 'ι',
    'kappa': 'κ',
    'lamda': 'λ',
    'mu': 'μ',
    'nu': 'ν',
    'omega': 'ω',
    'omicron': 'ο',
    'phi': 'φ',
    'pi': 'π',
    'psi': 'ψ',
    'rho': 'ρ',
    'sigma': 'σ',
    'tau': 'τ',
    'theta': 'θ',
    'upsilon': 'υ',
    'xi': 'ξ',
    'zeta': 'ζ'
}


def greek(letter_name):
    if letter_name in greek_letters_map:
        return greek_letters_map[letter_name]
    else:
        return None

    

def symbol(desc):
    _desc = desc.strip(" \/")
    if _desc == "alpha" or len(desc)==1 and desc=="a":
        return "α"
    if _desc == "gamma" or len(desc)==1 and desc=="g":
        return "γ"
    if _desc == "lambda" or len(desc)==1 and desc=="l":
        return "λ"
    if _desc == "nu" or len(desc)==1 and desc=="n":
        return "ν"
    if _desc == "rho" or len(desc)==1 and desc=="r":
        return "ρ"
    if _desc == "sigma" or len(desc)==1 and desc=="s":
        return "σ"


