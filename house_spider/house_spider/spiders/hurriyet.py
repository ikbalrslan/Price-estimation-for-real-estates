import scrapy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbs.hurriyet import Base, Hurriyet
from helper.image_fetch import imfetch

engine = create_engine('sqlite:///parsed.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class HurriyetSpider(scrapy.Spider):
    name = "hurriyet_spider"
    start_urls = [
        "https://www.hurriyetemlak.com/ankara-satilik/daire"
    ]
    log = open("invalid-parse-url_3.txt", "w")

    def parse(self, response):
        print(response.status)
        for link in response.css("a.overlay-link::attr(href)"):
            direct_url = response.urljoin(link.extract())
            yield response.follow(direct_url, self.parse_page)
        next_page = response.urljoin(response.css("a#lnkNext::attr(href)")[-1].extract())
        yield response.follow(next_page, self.parse)

    def parse_page(self, response):
        try:
            title = response.css("h1.details-header::text").extract_first()

            price = int(response.css("li.price-line").css("span::text").extract_first().replace(".", "").split(" ")[0])

            address_arr = response.css("span.address-line-breadcrumb")[0].css("a::text").extract()
            address = "/".join(address_arr)

            info_line = response.css("li.info-line ul.clearfix")[0]

            oda_salon_raw = info_line.css("li:contains('Oda +') span::text").extract()[1].split("+")
            oda_sayisi = int(oda_salon_raw[0]) + int(oda_salon_raw[1])

            genislik = int(info_line.css("li:contains('Metrekare') span::text").extract()[1].split(" ")[0].replace(".", ""))

            bina_yasi = int(info_line.css("li:contains('Bina Ya') span::text").extract()[1])

            kat_raw = info_line.css("li:contains('Bulundu') span::text").extract()[1]
            kat = int(kat_raw) if kat_raw.isdigit() else 0

            banyo_sayisi = int(info_line.css("li:contains('Banyo Sayısı') span::text").extract()[1])

            """ images """
            thumb_list = response.css("img.pretty::attr(src)").extract()
            # full_size_list = [thumb.replace("?type=4&", "?type=44&") for thumb in thumb_list]

            il_no = response.css("li.realty-numb").css("span::text").extract_first().split(" ")[-1]

        except Exception:
            print("an exception occured, skipping.")
            self.log.write(response.url)
            self.log.write("\n")
            return

        exists = session.query(Hurriyet).filter_by(ilan_no=il_no).first()
        if not exists:
            new_house = Hurriyet(
                link=response.url,
                title=title,
                price=price,
                ilan_no=il_no,
                yer=address,
                oda=oda_sayisi,
                metrekare=genislik,
                bina_yasi=bina_yasi,
                kat=kat,
                banyo=banyo_sayisi
            )
            session.add(new_house)
            session.commit()

            print("{} {} {} {} {} {} {} {}".format(
                title, price, address, oda_sayisi, genislik, bina_yasi, kat, banyo_sayisi
            ))

            # imfetch(full_size_list, il_no)
            imfetch(thumb_list, il_no)
