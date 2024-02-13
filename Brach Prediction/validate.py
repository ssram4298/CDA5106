import os 

os.system('python3 sim.py bimodal 6 ./traces/gcc_trace.txt > ./outputs/out_bimodal_1.txt')
os.system('python3 sim.py bimodal 12 ./traces/gcc_trace.txt > ./outputs/out_bimodal_2.txt')
os.system('python3 sim.py bimodal 4 ./traces/jpeg_trace.txt > ./outputs/out_bimodal_3.txt')
os.system('python3 sim.py gshare 9 3 ./traces/gcc_trace.txt > ./outputs/out_gshare_1.txt')
os.system('python3 sim.py gshare 14 8 ./traces/gcc_trace.txt > ./outputs/out_gshare_2.txt')
os.system('python3 sim.py gshare 11 5 ./traces/jpeg_trace.txt > ./outputs/out_gshare_3.txt')
os.system('python3 sim.py smith 3 ./traces/gcc_trace.txt > ./outputs/out_smith_1.txt')
os.system('python3 sim.py smith 1 ./traces/jpeg_trace.txt > ./outputs/out_smith_2.txt')
os.system('python3 sim.py smith 4 ./traces/perl_trace.txt > ./outputs/out_smith_3.txt')
os.system('python3 sim.py hybrid 8 14 10 5 ./traces/gcc_trace.txt > ./outputs/out_hybrid.txt')

print('Done running all test commands')
print("__________DIFF for Bimodal 1__________")
os.system('diff -w ./validation_runs/val_bimodal_1.txt ./outputs/out_bimodal_1.txt')
print("__________DIFF for Bimodal 2__________")
os.system('diff -w ./validation_runs/val_bimodal_2.txt ./outputs/out_bimodal_2.txt')
print("__________DIFF for Bimodal 3__________")
os.system('diff -w ./validation_runs/val_bimodal_3.txt ./outputs/out_bimodal_3.txt')
print("__________DIFF for Gshare 1___________")
os.system('diff -w ./validation_runs/val_gshare_1.txt ./outputs/out_gshare_1.txt')
print("__________DIFF for Gshare 2___________")
os.system('diff -w ./validation_runs/val_gshare_2.txt ./outputs/out_gshare_2.txt')
print("__________DIFF for Gshare 3___________")
os.system('diff -w ./validation_runs/val_gshare_3.txt ./outputs/out_gshare_3.txt')
print("__________DIFF for Smith 1____________")
os.system('diff -w ./validation_runs/val_smith_1.txt ./outputs/out_smith_1.txt')
print("__________DIFF for Smith 2____________")
os.system('diff -w ./validation_runs/val_smith_2.txt ./outputs/out_smith_2.txt')
print("__________DIFF for Smith 3____________")
os.system('diff -w ./validation_runs/val_smith_3.txt ./outputs/out_smith_3.txt')
print("__________DIFF for Hybrid_____________")
os.system('diff -w ./validation_runs/val_hybrid_1.txt ./outputs/out_hybrid.txt')