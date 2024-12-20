import sys, os
from libmagistri import *

URL = "https://bakaweb.cichnovabrno.cz/api/"

class object(object):
    def __iter__(self):
        return [self].__iter__()


class list(list):
    def __init__(self, value):
        try:
            return super().__init__(value)

        except TypeError:
            return eval(f"[value]", {})

    def e_to_string(self):
        list_ = []
        for i in self:
            list_.append(str(i))

        self = list_
        return list_


class str(str):
    def __init__(self, value):
        self.str = super().__init__(value)
        self.string = self.str(value)
        self = list(value)


def range(stop, start=0, step=1):
    i = start
    stop -= 1
    result = []
    while i <= stop:
        result.append(i)
        i += step

    return result


class int(int, object):
    pass


class dict(dict):
    def contains(self, key):
        if key in self:
            return True

        else:
            return False


def read(prompt, type=str, split=False, split_char=" "):
    input_ = input(prompt)
    if split:
        input_ = input_.split(split_char)
        for i in range(len(input_)):
            input_[i] = type(input[i])

        return input_

    else:
        return type(input_)


def exit(text=""):
    raise SystemExit(text)


if __name__ == "__main__":
    username = read("Zadej přihlašovací jméno: ")
    password = read("Zadej heslo: ")
    a = login(username, password)
    try:
        znamky = get_marks(a["access_token"])
        ukoly = get_hw(a["access_token"])
        rozvrh = get_ttable(a["access_token"])

    except KeyError as e:
        exit("Nesprávné přihlašovací jméno nebo heslo.")

    print("Vítej v programu Magistři.")
    print("Napiš 'help', 'napoveda' nebo 'pomoc' pro zobrazení nápovědy.")
    while True:
        command = read("(magistri) ")
        if command in ["help", "napoveda", "pomoc"]:
            print("Seznam příkazů: ")
            print("znamky - Vypíše známky.")
            print("ukoly - Vypíše domácí úkoly.")
            print("rozvrh - Vypíše rozvrh pro tento týden.")
            print("exit, ukoncit, konec - Ukončí tento program.")

        elif command == "znamky":
            if len(znamky) != 0:
                for i, j in znamky.items():
                    # print(j)
                    print(j["subject"]["Name"])
                    print("\nPrůměr: " + j["average"])
                    for k in j["marks"]:
                        print("Datum: " + k["MarkDate"])
                        print("Datum úpravy: " + k["EditDate"])
                        print(k["Caption"])
                        print("Známka: ", k["MarkText"] + "\n")
                        print("Váha: " + str(k["Weight"]))
                        if k["TypeNote"] != None:
                            print("Druh: " + k["TypeNote"])

                        print("\n")

                    print("\n")
            else:
                print("Vypadá to, že tady nic není.")

        elif command == "ukoly":
            if len(ukoly) != 0:
                for i in ukoly:
                    print("Od: " + i["start_date"])
                    print("Do: " + i["end_date"])
                    print("Třída: " + i["class"])
                    print("Předmět: " + i["subject"])
                    print("Učitel: " + i["teacher"])
                    print(i["contents"])
                    print("Hotovo: ", end="")
                    if i["finished"]:
                        print("Ano")
                    else:
                        print("Ne")
                    print("\n")
            else:
                print("Vypadá to, že tady nic není.")

        elif command == "rozvrh":
            for i in rozvrh:
                print(i + " ", " ")
                for k in range(2):
                    # print(k)
                    if k == 1:
                        print("  ", "  ")
                    for j in rozvrh[i]:
                        if len(j["subject"]) == 1:
                            start = " "
                            end = "  "

                        else:
                            start = ""
                            if len(j["subject"]) >= 3:
                                end = " "
                                if len(j["subject"]) == 4:
                                    subject = list(j["subject"])
                                    del subject[-1]
                                    j["subject"] = "".join(subject)

                            else:
                                end = "  "

                        if len(j["room"]) == 4:
                            room = list(j["room"])
                            del room[-1]
                            j["room"] = "".join(room)

                        if k == 0:
                            print(start + j["subject"], end)
                        else:
                            print(j["room"], " ")

                    print("")

        elif command in ["exit", "quit", "ukoncit", "zavrit"]:
            exit()

        else:
            print("Neznámý příkaz")
