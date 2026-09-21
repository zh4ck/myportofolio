<p align="center">
  <a href="https://opencode.ai">
    <picture>
      <img src="static/img/pyortofolio.png" alt="My portofolio logo xixi">
    </picture>
  </a>
</p>

<p align="center" style="color: #c3e3d6"><b>My personal portofolio for PBP courses.</b></p>
<p align="center">
  <a href="https://www.python.org"><img alt="django" src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" /></a>
  <a href="https://www.djangoproject.com/"><img alt="Build status" src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white" /></a>
  <a href="https://sqlite.org"><img alt="Build status" src="https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white" /></a>
</p>

<pre align="left">
Nama    : Zayyan Ramadzaki Firdaus
NPM     : 2506550955
Kelas   : PBP F
</pre>

## Deskripsi Project

Website ini merupakan portofolio pribadi saya yang sedang dikembangkan guna memenuhi penilaian PBP Semester Gasal 2026/2027. Portofolio saya mengandung identitas pribadi, latar belakang pendidikan saya, sedikit trivia mengenai saya, dan kemampuan yang saya punya.

Saat ini, website yang saya kembangkan masih bersifat statis dan sederhana. Pembaharuan akan dilakukan secara berkala, *so, stay tuned!*.

**Tech stack:**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

## Setup

Proyek ini membutuhkan Python 3.13 atau versi yang mendukung dependency pada [requirements.txt](requirements.txt), pastikan Python sudah ter-install, kemudian jalankan perintah berikut pada terminal direktori proyek untuk membuat *virtual environment*:

```bash
python -m venv env
```

Lalu aktifkan *virtual environment*:

> Untuk powershell
```bash
env\Scripts\Activate.ps1
```

>Untuk Command Prompt
```bash
env\Scripts\activate.bat
```

> Untuk terminal Vscode
```bash
env/Scripts/Activate
```

Install juga dependency yang dibutuhkan:

```bash
pip install -r requirements.txt
```

Jalankan Django's check dan migrasi database:

```bash
python manage.py check
python manage.py migrate
```

Lalu development server bisa dijalankan:

```bash
python manage.py runserver
```

Website sudah bisa diakses melalui http://127.0.0.1:8000 atau localhost anda. *Port mungkin berbeda tergantung ketersediaan port pada localhost anda*.

## Progres Mingguan

| Week | Progres |
| ------ | ------- |
| Week 1 | Melakukan setup Django & eksplorasi konsep dari Website |
| Week 2 | Menambahkan section baru (skills) dan mencoba deployment melalui PWS |

## Jawaban Tugas

### Tugas 1

1. Ya dan tidak, teruntuk bagian terluar yang menaungi page skills, saya menggunakan <section> untuk memastikan penggunaan elemen semantik yang mempermudah pembacaan struktur serta membantu SEO dan accessibility bagi yang membutuhkan, ini juga memisahkan antara profile dengan skills dan untuk bagian lainnya yang akan saya tambahkan kedepannya. Teruntuk hal lain seperti experience bar, saya hanya menggunakan <div> sederhana karena memang tidak memiliki makna semantik khusus, lebih ke arah layout wrapper saja untuk mengatur tampilan. Untuk elemen semantik lainnya seperti `<article>` atau `<aside>` belum saya gunakan karena untuk sekarang masih belum ada sidebar atau elemen yang berperan sebagai suatu artikel.
2. Tantangan utama mungkin terletak pada mengatur width setiap elemen agar bisa menyesuaikan ukuran viewport, untuk itu saya menggunakan `clamp` pada CSS yang digabungkan dengan satuan `vw` (viewport) yang akan menyesuaikan dengan ukuran viewport, mengambil value yang tepat agar tetap responsif. *Kalau pakai Tailwind sih enak ya bisa pakai `lg:`, `md:`, dan sebagainya 😹*. Perihal penentuan elemen yang diprioritaskan, saya kurang lebih menguji terkait ada/tidaknya horizontal scrolling, apakah suatu teks dapat terbaca di berbagai viewport, apakah gambar tetap proporsional, apakah informasi utama seperti nama dan profile picture masih menjadi "highlight", apakah navigasi mudah untuk dilakukan (UX), dan sebagainya.
3. Menurut saya, keterbatasan utama terletak pada interaktivitas antara pengunjung dengan website. Informasi yang ingin ditampilkan harus ditulis langsung pada file HTML sehingga konten masih belum dinamis. Untuk kedepannya mungkin saya akan menambahkan hal yang lumayan generik - tidak lain dan tidak bukan adalah switch *dark mode* dan *light mode*, juga kemampuan untuk menyimpan preferensi pengunjung tersebut jadi saat mereka berkunjung kembali ke website saya, pengaturan sebelumnya (misal mereka toggle menjadi dark mode) sudah tersimpan dan tidak perlu di toggle kembali. Diluar hal tersebut, saya ingin bereksperimen dengan penggunaan database, sepertinya akan dipelajari di pekan selanjutnya mengenai SQLite, ini juga memungkinkan untuk filtering project, forms, dan sebagainya. Ditunggu tugas selanjutnya xoxo!

Anyway, saya **"Tidak menggunakan AI"**. Problem-solving saya lebih ke arah langsung bereksperimen dengan apa yang saya ingin lakukan ya, kalau ada yang salah, coba cari tahu salahnya dimana, fix, repeat, sampai benar sesuai kemauan saya. Website yang saya gunakan sebagai panduan mungkin seperti [Mozilla Developer Network (MDN)](https://developer.mozilla.org/en-US/) dan [W3Schools](https://www.w3schools.com/) ya, kadang [GeeksForGeeks](http://geeksforgeeks.org/) karena ada beberapa blog yang jelasin cara styling sesuatu dengan CSS. Alasan saya tidak menggunakan AI untuk penugasan kali ini adalah dikarenakan untuk hal dasar seperti ini menurut saya bukanlah suatu hal yang baik untuk dilakukan, materi dasar seperti HTML dan CSS sangatlah krusial sebagai pondasi untuk tugas dan tutorial kedepannya, sehingga alangkah lebih baiknya untuk menggunakan kemampuan diri sendiri dan mengasah kemampuan *problem-solving* agar lebih kritis. Lagipula suatu karya yang dihasilkan oleh tangan sendiri akan terasa lebih hidup dan *satisfying* dibandingkan melempar langsung selera styling kepada GenAI. Sedikit tambahan, saya juga sudah pernah mencoba untuk mempergunakan AI pada beberapa proyek yang melibatkan tech stack yang jauh lebih rumit (framework), banyak kejadian dimana AI berhalusinasi, menggunakan API yang tidak pernah ada, melakukan duplikasi blok kode, memberikan solusi yang tidak human-readable, mustahil untuk dipahami kecuali berotak senku, dan semacamnya. Memang betul development akan menjadi lebih lama tanpa bantuan AI, tetapi apa gunanya deliver dengan buru-buru, kalau tidak berkualitas? As always, *Quality over Quantity*.

### Tugas 2

1. Ketika saya buka halaman baru misalnya `/project/`, browser mengirim HTTP request ke server Django. Nantinya request itu bakal dihandle sama `portofolio/urls.py` dimana isinya ada untuk  `admin/` dan juga untuk `main.urls` yang nantinya bakal ngelempar request lainnya ke `main/urls.py`. Jadi kurang lebih ini kyk bedain mana user mana admin sih, sisanya dihandle sama `main/urls.py` dimana nanti bakal dikasih tuh routingnya kemana aja, misal project nanti ke page project, experience ke experience, ibarat route.ts kalo di framework tsx :v. Nantinya pas project udah di route via `urls.py`, nanti Django panggil fungsi `show_project` yang bakal ngarah ke `main/views.py`, nantii dia ngambil data dari model `Projects.objects.all()` kyk di iterate tiap objek yang ada dengan urutan dari tanggal terbaru hingga tanggal terlama. Terus nanti view manggil `render(request, "project.html", context)` buat ngerender si page `project.html` dimana didalemnya ada iterasi buat setiap project yang ada di project list `{% for project in project_list %}`, terus ambil semua fields yang ada, terus dikirim as `HttpResponse` baru di render deh nantinya.
2. Kalau data ditulis langsung di template, setiap kali saya mau nambah, ubah, atau hapus satu project, saya kan harus buka file `.html` nya terus atur sendiri ya manual, padahal strukturnya mirip mirip (foto, nama, tanggal, deskripsi). Ini bikin proses development jadi gak efektif sih, hal yang iteratif, sama, harusnya kan bisa dipercepat ya, dipermudah gitu. Jadinya dengan definisiin fieldnya sekali aja kyk `name`, `description`, `category` dan lainnya, nanti template tinggal loop ke semua objek yang ada terus ambil tiap field yang dibutuhkan deh. Oiya dengan pake model juga bikin saya bisa lakuin hal yang agak susah/tricky kalau pure HTML, kyk misalkan mau urutin project dari yang terbaru `order_by("-date_start")`, atau nanti filtering berdasarkan kategori. Dari sisi maintenance, kalau saya mau ganti struktur (misal nambah field baru) ya saya tinggal tambahin field di `models.py` terus di migrate deh, dibanding Ctrl + F semua halaman HTML yang contains data itu. Intinya, pemisahan data dan tampilan ini bikin kodenya lebih *scalable* dan gampang dites (pake unit test kyk di `tests.py`).
3. `makemigrations` itu tugasnya membandingkan model Python saya sekarang dengan riwayat migration terakhir, terus menghasilkan file migration baru (isinya operasi seperti `AddField`, `AlterField`, dsb) tapi ini gak ngubah database sama sekali, cuma nulis perubahan yang ada ke file Python di folder `migrations/`. Nah baru pas dijalanin `migrate` dia bakal ubah skema yang ada di database, jalanin perintah SQL kyk `ALTER TABLE` untuk nambah/ubah kolom sama catat migration mana saja yang udah diterapin supaya gak dijalanin dua kali. Contoh nyata yang saya alami tadi misalnya pas tambahin field `thumbnail` (`URLField`) ke model `Projects` supaya tiap project bisa punya foto. Abis ubah `models.py` terus run `python manage.py makemigrations main`, nanti bakal generate file `0004_projects_thumbnail.py` terus tinggal `python manage.py migrate main` biar kolom `thumbnail` dibuat nanti di tabel `main_projects`.

Seperti biasa, saya tidak menggunakan AI / GenAI / LLM untuk Tugas ini karena kebetulan masih bisa saya handle hohoho, lagipula seru juga :3

### Tugas 3

1. Alasan utama pake `ModelForm` ya jelas sih biar gak nulis form HTML secara manual satu-satu. Bayangin kalau form-nya panjang, tiap field harus ketik manual `<input>`, `<label>`, attribute `name` yang harus match sama model, terus nanti pas di view-nya juga harus validasi manual satu-satu (`name kosong gak?`, `date-nya valid gak?`), ribet parah. Dengan `ModelForm`, saya cuma perlu define `model = Projects` dan `fields = [...]` di `forms.py`, nanti Django otomatis generate form-nya berdasarkan field yang ada di model, lengkap sama tipe input yang sesuai, dan validasinya juga jalan otomatis pas saya panggil `form.is_valid()`. Jadi berkurang drastis tuh boilerplate-nya, plus kode jadi lebih DRY karena kalau model berubah (misal tambah field baru), form-nya tinggal update list `fields`-nya doang, gak perlu utak-atik HTML manual. Terus soal `{% csrf_token %}`, ini wajib karena Django secara default punya proteksi terhadap serangan **CSRF (Cross-Site Request Forgery)**. Singkatnya, CSRF itu serangan dimana attacker bisa "memalsukan" request dari browser kita ke server tanpa kita sadari, misalnya kita lagi login terus gak sengaja buka website jahat, website itu bisa diam-diam kirim POST request ke server kita pakai session kita yang masih aktif. Dengan `{% csrf_token %}`, Django bakal generate token unik yang diselipin di form, dan nanti saat form di-submit, server bakal verifikasi apakah token itu valid atau bukan. Kalau gak ada token ini, request POST bakal ditolak sama Django (403 Forbidden) karena dianggap tidak berasal dari form yang legitimate. Jadi intinya ini lapisan keamanan yang gak boleh dilewatin, karena kalau skip, data kita jadi rentan dimanipulasi sama pihak yang gak bertanggung jawab.

2. Menurut saya, JSON lebih disukai dibanding XML karena beberapa hal fundamental. Pertama dari segi sintaks, JSON itu jauh lebih *lightweight* dan readable, strukturnya key-value dengan array dan object, mirip banget sama cara nulis object di JavaScript atau dictionary di Python, jadi gak heran kalau parsing-nya cepet dan gak berat. Bandingkan sama XML yang harus buka-tutup tag `</tag>` terus tiap elemen, verbose parah, payload-nya jadi bengkak gak perlu, dan kalau datanya besar, bandwidth yang kepakai juga lebih boros. Kedua, dari sisi *native support*, JSON itu literally didukung secara native sama hampir semua bahasa pemrograman modern, apalagi JavaScript yang notabene jadi tulang punggung web development, jadi `JSON.parse()` atau `JSON.stringify()` udah built-in, gak perlu library tambahan. XML butuh parser khusus dan lebih ribet handling-nya. Ketiga, JSON lebih *flexible* karena strukturnya gak butuh skema yang rigid kayak XML yang butuh DTD/XSD kalau mau strict, JSON bisa langsung dipakai tanpa define skema dulu, jadi lebih *developer-friendly* buat iterasi cepet. Ditambah lagi, ekosistem web modern (REST API, fetch, dsb) udah terlanjur standarisasi JSON sebagai format default, jadi ya natural aja semua orang pake itu. XML masih ada sih gunanya di konteks tertentu kayak SOAP atau dokumen yang butuh markup semantik, tapi untuk kebutuhan API dan pertukaran data di web modern, JSON udah menang telak.

3. Alurnya kurang lebih begini: pertama user ngirim request (misalnya GET ke endpoint `json/`), terus request itu di-route sama `urls.py` ke fungsi view yang nge-handle JSON response. Di dalam view itu, saya ambil data dari model pakai `Projects.objects.all()` (atau filter tertentu), yang hasilnya itu berupa QuerySet berisi object-object Python dari model Django. Nah, masalahnya object model Django ini **gak bisa langsung** dikirim sebagai response HTTP, karena response HTTP itu cuma bisa ngirim data dalam bentuk string/bytes yang terstruktur (misalnya JSON, XML, HTML). Di sinilah proses **serialization** dibutuhkan, yaitu mengubah object Python (model instance) menjadi format yang bisa ditransmisikan, dalam hal ini dictionary/JSON. Caranya bisa pake `serializers.serialize("json", queryset)` bawaan Django, atau kalau lebih custom ya iterasi manual tiap objek terus masukin field-fieldnya ke dict terus `JsonResponse`. Setelah data udah ke-serialize jadi JSON, baru deh view return `JsonResponse` atau `HttpResponse` dengan `content_type="application/json"`, nanti dikirim balik ke client. Kenapa harus di-serialize? Karena model Django itu basically representasi ORM dari row di database, dia punya method, attribute khusus, koneksi ke database, dan semacamnya, yang semuanya itu gak relevan dan gak bisa direpresentasikan dalam format teks seperti JSON. Kalau kita coba langsung return objek model tanpa di-serialize, bakal error karena Django gak tau cara "mendownload" objek Python itu jadi bytes yang bisa dikirim lewat HTTP. Selain itu, serialization juga penting buat keamanan dan privasi, kita bisa milih field mana aja yang mau di-expose ke client, jadi gak semua data internal kebocor ke luar. Intinya, serialization itu "jembatan" antara dunia object Python di server dengan dunia data terstruktur yang bisa dikonsumsi client (browser, mobile app, dll).
