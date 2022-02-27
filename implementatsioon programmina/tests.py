from seos import *

A=Predikaat("A")
B=Predikaat("B")

assert str(LV(E(~A(1, 1) & E(A(1, 2) & ~A(2, 1) & ~A(2, 2) & E(~A(1, 3) & A(2, 3) & ~A(3, 1) & ~A(3, 2) & ~A(3, 3)) & E(~A(1, 3) & A(2, 3) & ~A(3, 1) & ~A(3, 2) & A(3, 3)))) & ~E(~A(1, 1) & E(~A(1, 2) & A(2, 1) & ~A(2, 2) & E(A(1, 3) & ~A(2, 3) & ~A(3, 1) & ~A(3, 2) & ~A(3, 3)) & E(A(1, 3) & ~A(2, 3) & ~A(3, 1) & ~A(3, 2) & A(3, 3))))))=="¬∃(¬A(1,1) & ∃(¬A(1,2) & A(2,1) & ¬A(2,2) & ∃(A(1,3) & ¬A(2,3) & ¬A(3,1) & ¬A(3,2) & ¬A(3,3)) & ∃(A(1,3) & ¬A(2,3) & ¬A(3,1) & ¬A(3,2) & A(3,3)))) & ∃(¬A(1,1) & ∃(A(1,2) & ¬A(2,1) & ¬A(2,2) & ∃(¬A(1,3) & A(2,3) & ¬A(3,1) & ¬A(3,2) & ¬A(3,3)) & ∃(¬A(1,3) & A(2,3) & ¬A(3,1) & ¬A(3,2) & A(3,3))))"

if False:
    on_null = Predikaat("on_null")
    võrdne = Predikaat("võrdne")
    PEANO = E(on_null(1)) & \
            ~E(~võrdne(1, 1)) & \
            ~E(E(E(~((võrdne(1, 2) & võrdne(2, 3)) >> võrdne(3, 1)))))
    peano_puu = LV(PEANO).mitte_ÜV()
    print("Peano tulem:", peano_puu)
    print("\n#####\n")

A = Predikaat("A")
B = Predikaat("B")
# print(koosta_puu(E(A(1) & A(1, 1) & E(A(1, 2) & E(A(2, 3) & A(3, 1))))))

if True:  # võituste välja viimine ilma ÜV-kontrolliteta.
    print("################################\nTESTS:")
    sisendid = [~E(A(21) & A(22) & A(23)), E(E(E(E(A(0) | A(1) | A(2))))),
                (E(A(30) & A(31)) | (A(33) & E(A(40) | A(41) & E(E(E(A(51) | A(53))))))),
                ~E(A(1) & A(2)),
                ~E(A(1) | A(2) & A(3)) & E(A(4) & A(5) & E(A(6))),
                A(10) & E(A(11) >> A(12) & ~E(A(13) | A(14) & ~E(A(10) & A(20)))),
                E(võrdne(0) & on_null(2) & on_null(1)),
                ~E(A(2) << A(1)), E(A(1) | A(2)) & E(A(1) | A(2))]
    oodatud = ["[(¬∃((A(21) & A(22) & A(23))))]",
               "[(∃((∃((∃((∃((A(0)))))))))), (∃((∃((∃((∃((A(1)))))))))), (∃((∃((∃((∃((A(2))))))))))]",
               "[(∃((A(30) & A(31)))), (A(33)&∃((A(40)))), (A(33)&∃((A(41)&∃((∃((∃((A(51)))))))))), (A(33)&∃((A(41)&∃((∃((∃((A(53))))))))))]",
               "[(¬∃((A(1) & A(2))))]",
               "[(¬∃((A(1)))&¬∃((A(2) & A(3)))&∃((A(4) & A(5)&∃((A(6))))))]",
               "[(A(10)&∃((A(12)&¬∃((A(13)))&¬∃((A(14)&¬∃((A(10) & A(20)))))))), (A(10)&∃((¬A(11)&¬∃((A(13)))&¬∃((A(14)&¬∃((A(10) & A(20))))))))]",
               "[(∃((on_null(1) & on_null(2) & võrdne(0))))]",
               "[(¬∃((A(2)))&¬∃((¬A(1))))]",
               "[(∃((A(1)))), (∃((A(2))))]"]
    for i in range(max(len(sisendid), len(oodatud))):
        tulemus = str(LV.koosta_puu(sisendid[i]))
        if tulemus != oodatud[i]:
            print("SISEND :", sisendid[i])
            print("TULEMUS:", tulemus)
            print("OODATUD:", oodatud[i])
            print()
            # print(sisendid[i],":",tulemus,":",oodatud[i])
        print()
    # proov=mitte_ÜV(U(A(0)&A(1)&U(A(3)&A(4)&U(A(5)))&~U(A(21)&A(22)&U(A(23))&~U(A(24)|A(25)))))
    # print("proov:",mitte_ÜV(U(U(on_null(2))&U(võrdne(2,2)))))
    # proov2=mitte_ÜV(U(U(U(U(A(0)&A(1)&A(2))))))
    #    proov2=mitte_ÜV(~U(A(0) | A(1) | A(2)))
    # print("proov:", proov2)