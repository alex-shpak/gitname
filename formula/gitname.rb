# This file was generated by GoReleaser. DO NOT EDIT.
class Gitname < Formula
  desc "Simple script to set git config properties in git repository based on remote url."
  homepage "https://github.com/alex-shpak/gitname"
  version "5"
  bottle :unneeded

  if OS.mac?
    url "https://github.com/alex-shpak/gitname/releases/download/v5/gitname_5_Darwin_x86_64.tar.gz"
    sha256 "9419da7acf1812bc760ea604e76cbf9aa4cef4def9e11c0abd8bb0d2ca18714b"
  elsif OS.linux?
    if Hardware::CPU.intel?
      url "https://github.com/alex-shpak/gitname/releases/download/v5/gitname_5_Linux_x86_64.tar.gz"
      sha256 "58bca3dc68fe934561443b3d4ad1518e18502277f93c9af0eabe5be47bc971cf"
    end
  end
  
  depends_on "git"

  def install
    bin.install "gitname"
  end
end
