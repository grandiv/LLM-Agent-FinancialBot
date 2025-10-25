"""
Test just the parser with sample data
"""

import sys
import codecs

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from core.mcp_manager import MCPManager

# Sample raw search result (like what you showed)
SAMPLE_RAW = """Search completed for "iPhone 17 Pro Max harga Indonesia price" with 3 results:

**Status:** Search engine: Browser Brave; 3 result requested/8 obtained; PDF: 0; 8 followed; Successfully extracted: 3; Failed: 0; Results: 3

**1. KOMPAS.com   tekno.kompas.com   › gadget  Harga iPhone 17 Pro Max di Indonesia dan Spesifikasinya, Mulai Rp 25 Jutaan**
URL: https://tekno.kompas.com/read/2025/10/10/14350067/harga-iphone-17-pro-max-di-indonesia-dan-spesifikasinya-mulai-rp-25-jutaan
Description: 2 weeks ago - Harga iPhone 17 Pro Max di Indonesia dipatok mulai Rp 25 jutaan. Spesifikasi iPhone 17 Pro Max mencakup kamera 48 MP dan chip Apple A19 Pro.

**Full Content:**
Harga iPhone 17 Pro Max di Indonesia dipatok mulai Rp25.999.000 untuk varian 256GB. Varian 512GB dijual Rp29.999.000, sedangkan varian 1TB dibanderol Rp35.999.000.

---

**2. Kumparan   kumparan.com   › tekno & sains  › berita hari ini  › harga iphone 17 pro max di indonesia beserta spesifikasinya      Harga iPhone 17 Pro Max di Indonesia beserta Spesifikasinya | kumparan.com**
URL: https://kumparan.com/berita-hari-ini/harga-iphone-17-pro-max-di-indonesia-beserta-spesifikasinya-2654NHMlukf
Description: 5 days ago - Dikutip dari laman resmi iBox selaku ... penyimpanan. Untuk model tertinggi, iPhone 17 Pro Max, harganya mencapai Rp 43.999.000 pada varian 2 TB....

**Full Content:**
LoadingLoadingLoadingLoadingLoadingLoadingLoadingLoadingLoadingLoadingLainnyaVideo StoryGaleri FotoKabar DaerahPollingZodiakTentang KamiPedoman Media SiberKetentuan & Kebijakan PrivasiPanduan KomunitasPeringkat PenulisCara Menulis di kumparanInformasi Kerja SamaBantuanIklanKarirInstagramFacebookTiktokYoutubeWhatsappX2025 iPhone 17 Pro Max 256GB Rp27.499.000, iPhone 17 Pro Max 512GB Rp31.999.000, varian 2TB mencapai Rp43.999.000

**3. iBox Indonesia - Official Apple Premium Reseller**
URL: https://www.ibox.co.id/iphone-17-pro-max
Description: iPhone 17 Pro Max tersedia di iBox Indonesia

**Full Content:**
Pre-order iPhone 17 Pro Max sekarang! Harga mulai Rp26.999.000 untuk 256GB. Cicilan 0% tersedia. Gratis ongkir seluruh Indonesia."""

mcp = MCPManager()
result = mcp._parse_search_results(SAMPLE_RAW, "iPhone 17 Pro Max")

print("="  * 60)
print("FORMATTED OUTPUT:")
print("=" * 60)
print(result)
print("=" * 60)
