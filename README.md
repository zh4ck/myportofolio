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