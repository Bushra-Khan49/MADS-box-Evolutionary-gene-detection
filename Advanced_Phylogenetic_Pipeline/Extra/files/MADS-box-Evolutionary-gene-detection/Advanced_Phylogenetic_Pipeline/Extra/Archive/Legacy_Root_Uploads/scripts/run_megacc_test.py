import os
import shutil
import subprocess

def run():
    sandbox = "/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK/test_sandbox"
    os.makedirs(sandbox, exist_ok=True)
    
    # Copy files
    shutil.copy("/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK/scripts/nj_tree_500.mao", os.path.join(sandbox, "nj.mao"))
    shutil.copy("/Users/bushrakhan/Desktop/NIPGR-data/NIPGR_WORK/Amborella_trichopoda/Amborella_trichopoda_cleaned.meg", os.path.join(sandbox, "data.meg"))
    
    # Run megacc
    cmd = ["/usr/local/bin/megacc", "-a", "nj.mao", "-d", "data.meg", "-o", "sandbox_out"]
    try:
        result = subprocess.run(cmd, cwd=sandbox, capture_output=True, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        print("EXIT CODE:", result.returncode)
    except Exception as e:
        print("ERROR:", str(e))

if __name__ == "__main__":
    run()
