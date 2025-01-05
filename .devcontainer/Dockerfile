FROM fedora:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN dnf update -y \
&& dnf install -y helix neovim git fd-find fzf ripgrep sd

RUN dnf copr enable -y atim/lazygit \
&& dnf install -y lazygit

RUN dnf copr enable -y atim/starship \
&& dnf install -y starship \
&& echo 'eval "$(starship init bash)"' >> /root/.bashrc

WORKDIR /workspace

CMD ["/bin/bash"]
