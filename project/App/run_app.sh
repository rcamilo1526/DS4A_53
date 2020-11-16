pip install -r requirements.txt
nohup streamlit run catastro.py > my.log 2>&1 &
echo $! > save_pid.txt
