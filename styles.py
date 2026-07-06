def load_css():
    return """
    <style>

    /* Hide Streamlit Menu */
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}

    .stApp{
        background:#0E1117;
        color:white;
    }

    /* Hero Banner */
    .hero{
        background:linear-gradient(
            rgba(0,0,0,.85),
            rgba(0,0,0,.90)
        ),
        url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1600");
        background-size:cover;
        background-position:center;
        padding:70px;
        border-radius:20px;
        margin-bottom:30px;
    }

    .hero h1{
        color:#E50914;
        font-size:55px;
        font-weight:800;
        margin-bottom:10px;
    }

    .hero p{
        font-size:20px;
        color:#DDDDDD;
    }

    /* Search Box */

    input{
        border-radius:12px !important;
    }

    /* Recommendation Button */

    .stButton>button{
        background:#E50914;
        color:white;
        border:none;
        border-radius:10px;
        height:50px;
        width:100%;
        font-size:18px;
        font-weight:bold;
    }

    .stButton>button:hover{
        background:#B20710;
        transition:.3s;
    }

    /* Movie Card */

    .movie-card{

        background:#181818;
        border-radius:15px;
        padding:15px;

        transition:0.3s;
    }

    .movie-card:hover{

        transform:scale(1.05);

        box-shadow:0px 8px 30px rgba(255,255,255,.15);
    }

    </style>
    """
