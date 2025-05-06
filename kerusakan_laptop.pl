:- use_module(library(pce)).
:- dynamic(yes/1).
:- dynamic(no/1).

% ===== Interface GUI =====
start :-
    new(Dialog, dialog('Sistem Pakar - Deteksi Kerusakan Laptop')),
    send(Dialog, append, new(_, text('Selamat datang di sistem pakar deteksi kerusakan laptop.'))),
    send(Dialog, append, new(_, button('Mulai Diagnosa', message(@prolog, mulai_diagnosa, Dialog)))),
    send(Dialog, append, new(_, button('Keluar', message(Dialog, destroy)))),
    send(Dialog, open).

% ===== Aturan Diagnosa =====
mulai_diagnosa(Dialog) :-
    send(Dialog, destroy),
    (   kerusakan(Kerusakan) ->
        show_result(Kerusakan)
    ;   show_result('Maaf, kerusakan tidak dapat dikenali.')
    ),
    undo.

% ===== Basis Pengetahuan =====
kerusakan('Kipas Rusak') :-
    tanya(kipas_berbunyi_tidak_normal),
    tanya(laptop_cepat_panas).

kerusakan('RAM Bermasalah') :-
    tanya(sering_blue_screen),
    tanya(laptop_lambat_sekalipun_spesifikasi_bagus).

kerusakan('Harddisk Rusak') :-
    tanya(suara_aneh_dari_harddisk),
    tanya(file sıring_korup).

kerusakan('Battery Rusak') :-
    tanya(baterai_tidak_mengisi),
    tanya(laptop_mati_saat_charger_dicabut).

kerusakan('LCD Bermasalah') :-
    tanya(tampilan_bergaris),
    tanya(layar_berkedip).

% ===== Tanya Gejala ke Pengguna =====
tanya(Gejala) :-
    (yes(Gejala) ->
        true
    ; no(Gejala) ->
        fail
    ; ask(Gejala)).

ask(Gejala) :-
    atom_concat('Apakah ', Gejala, T1),
    atom_concat(T1, '?', Pertanyaan),
    new(D, dialog('Pertanyaan')),
    send(D, append, label(question, Pertanyaan)),
    send(D, append, button(ya, message(D, return, yes))),
    send(D, append, button(tidak, message(D, return, no))),
    send(D, default_button, ya),
    get(D, confirm, Answer),
    send(D, destroy),
    (   Answer == yes ->
        assertz(yes(Gejala))
    ;   assertz(no(Gejala)), fail).

% ===== Tampilkan Hasil =====
show_result(Result) :-
    new(D, dialog('Hasil Diagnosa')),
    send(D, append, label(result, string('Kerusakan yang terdeteksi: %s', Result))),
    send(D, append, button(tutup, message(D, destroy))),
    send(D, open).

% ===== Reset Fakta Sementara =====
undo :- retract(yes(_)), fail.
undo :- retract(no(_)), fail.
undo.
