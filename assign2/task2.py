import pandas as pd 
import matplotlib.pyplot as plt
from task1 import generate_subkeys, des_encrypt_block, hex_to_bitlist, feistel_function

def count_bit_diff(hex1, hex2):
    """Count differing bits between two hex strings of equal length."""
    b1 = hex_to_bitlist(hex1, len(hex1)*4)
    b2 = hex_to_bitlist(hex2, len(hex2)*4)
    return sum(x != y for x, y in zip(b1, b2))

def run_spac(plaintext1, plaintext2, key):
    subkeys = generate_subkeys(key)
    diffs = []
    for r in range(1, 17):
        c1 = des_encrypt_block(plaintext1, subkeys, rounds=r)
        c2 = des_encrypt_block(plaintext2, subkeys, rounds=r)
        diffs.append(count_bit_diff(c1, c2))
    return diffs

# --- SKAC (Strict Key Avalanche Criterion) ---
def run_skac(plaintext, key1, key2):
    subkeys1 = generate_subkeys(key1)
    subkeys2 = generate_subkeys(key2)
    diffs = []
    for r in range(1, 17):
        c1 = des_encrypt_block(plaintext, subkeys1, rounds=r)
        c2 = des_encrypt_block(plaintext, subkeys2, rounds=r)
        diffs.append(count_bit_diff(c1, c2))
    return diffs

def main():
    pt1 = "0123456789ABCDEF"
    key1 = "133457799BBCDFF1"

    pt2 = "0123456789ABCDEF"
    key2 = "133457799BBCDFF1"

    spac_diffs = run_spac(pt1, pt2, key1)
    df_spac = pd.DataFrame({"Round": range(1, 17), "Bit Differences": spac_diffs})
    df_spac.to_csv("SPAC.csv", index=False)

    # Run SKAC
    skac_diffs = run_skac(pt1, key1, key2)
    df_skac = pd.DataFrame({"Round": range(1, 17), "Bit Differences": skac_diffs})
    df_skac.to_csv("SKAC.csv", index=False)

     # Graph for SPAC
    plt.figure()
    plt.plot(range(1, 17), spac_diffs, marker="o", linestyle="-", color="blue", label="SPAC")
    plt.xlabel("Round")
    plt.ylabel("Differing Bits")
    plt.title("Strict Plaintext Avalanche Criterion (SPAC)")
    plt.xticks(range(1, 17))
    plt.legend()
    plt.grid(True)
    plt.savefig("SPAC.png")

    # Graph for SKAC
    plt.figure()
    plt.plot(range(1, 17), skac_diffs, marker="s", linestyle="--", color="red", label="SKAC")
    plt.xlabel("Round")
    plt.ylabel("Differing Bits")
    plt.title("Strict Key Avalanche Criterion (SKAC)")
    plt.xticks(range(1, 17))
    plt.legend()
    plt.grid(True)
    plt.savefig("SKAC.png")


if __name__ == "__main__":
  main() 
