import subprocess

done = 0
failed = 0

elements = [
    "login",
    "mainmenu",
    "conflicts",
    "order",
    "order_lineitem",
    "warehouse",
    "customers",
]
#elements = ["conflicts"]

print("====================================================")
print("==   creating python ui elements from .ui files   ==")
print("====================================================")
print()

for element in elements:
    try:
        subprocess.check_output(
            "pyuic5 -x ./viewports/" + element + ".ui -o ./viewports/" + element + ".py"
        )
        print("OK       " + element + "-window done")
        done += 1
    except:
        print("FAILED   " + element + "-window")
        failed += 1

print("\nconvertion finished")
print(str(done) + " done - " + str(failed) + " failed")
if failed == 0:
    print("\ncreation successful")
else:
    print("\ncreation failed with " + str(failed) + " ERROR(S)")
