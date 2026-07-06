def load_css():

    return """

<style>

/* ------------------------------------------------------- */
/* GENERAL */
/* ------------------------------------------------------- */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

html, body, [class*="css"]{

    background:#0B0B0B;
    color:white;
    font-family:Arial, Helvetica, sans-serif;

}

.stApp{

    background:#0B0B0B;

}

/* ------------------------------------------------------- */
/* HERO */
/* ------------------------------------------------------- */

.hero{

    background:
    linear-gradient(
        rgba(0,0,0,.82),
        rgba(0,0,0,.95)
    ),

    url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1600");

    background-size:cover;
    background-position:center;

    padding:80px;

    border-radius:20px;

    margin-bottom:35px;

}

.hero h1{

    color:#E50914;

    font-size:60px;

    font-weight:800;

}

.hero p{

    color:#DDDDDD;

    font-size:20px;

}

/* ------------------------------------------------------- */
/* BUTTON */
/* ------------------------------------------------------- */

.stButton>button{

    background:#E50914;

    color:white;

    border:none;

    border-radius:10px;

    width:100%;

    height:52px;

    font-size:18px;

    font-weight:bold;

}

.stButton>button:hover{

    background:#B20710;

    transition:0.25s;

}

/* ------------------------------------------------------- */
/* SEARCH */
/* ------------------------------------------------------- */

.stTextInput>div>div>input{

    background:#222;

    color:white;

    border-radius:12px;

}

/* ------------------------------------------------------- */
/* MOVIE CARD */
/* ------------------------------------------------------- */

.movie-card{

    background:#171717;

    border-radius:18px;

    padding:12px;

    transition:0.3s;

    min-height:610px;

}

.movie-card:hover{

    transform:translateY(-8px);

    box-shadow:0px 10px 35px rgba(255,255,255,.15);

}

/* ------------------------------------------------------- */
/* MOVIE TITLE */
/* ------------------------------------------------------- */

.movie-title{

    font-size:20px;

    font-weight:bold;

    margin-top:10px;

    color:white;

}

/* ------------------------------------------------------- */
/* BADGES */
/* ------------------------------------------------------- */

.badge{

    display:inline-block;

    padding:5px 12px;

    border-radius:20px;

    margin:3px;

    font-size:13px;

    color:white;

}

.rating{

    background:#28a745;

}

.year{

    background:#0d6efd;

}

.runtime{

    background:#fd7e14;

}

.genre{

    background:#6f42c1;

}

/* ------------------------------------------------------- */
/* POSTER */
/* ------------------------------------------------------- */

.movie-poster{

    border-radius:15px;

    width:100%;

}

/* ------------------------------------------------------- */
/* SIDEBAR */
/* ------------------------------------------------------- */

section[data-testid="stSidebar"]{

    background:#111;

}

/* ------------------------------------------------------- */
/* EXPANDER */
/* ------------------------------------------------------- */

details{

    background:#1B1B1B;

    border-radius:10px;

    padding:10px;

}

/* ------------------------------------------------------- */
/* SCROLLBAR */
/* ------------------------------------------------------- */

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-thumb{

    background:#E50914;

    border-radius:20px;

}

</style>

"""
