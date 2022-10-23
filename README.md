# gym-dssat-setup

## Steps to start the gym-dssat container
```bash
docker run -it --name jammy2 ubuntu:jammy

apt update -y
apt upgrade -y
apt install -y wget

echo "deb [ arch=amd64 ] https://raw.githubusercontent.com/pdidev/repo/ubuntu jammy main" | tee /etc/apt/sources.list.d/pdi.list > /dev/null
wget -O /etc/apt/trusted.gpg.d/pdidev-archive-keyring.gpg https://raw.githubusercontent.com/pdidev/repo/ubuntu/pdidev-archive-keyring.gpg
chmod a+r /etc/apt/trusted.gpg.d/pdidev-archive-keyring.gpg /etc/apt/sources.list.d/pdi.list

apt update -y
apt install -y pdidev-archive-keyring

wget https://gac.udc.es/~emilioj/jammy.tgz
tar -xf jammy.tgz
cd /jammy
apt install -y `find . -name "*.deb"`

export VIRTUAL_ENV=/opt/gym_dssat_pdi
export PATH="${VIRTUAL_ENV}/bin:${PATH}"

echo "export PATH=${PATH}" >> /etc/profile
bash -l -c 'echo export GYM_DSSAT_PDI_PATH="/opt/gym_dssat_pdi/lib/$(python3 -V | tr -d '[:blank:]' | tr '[:upper:]' '[:lower:]' | sed 's/\.[^.]*$//')/site-packages/gym_dssat_pdi" >> /etc/bash.bashrc'

useradd -ms /bin/bash gymusr
su gymusr
cd /home/gymusr

export BASH_ENV=/etc/profile

bash -c "python /opt/gym_dssat_pdi/samples/run_env.py"
```