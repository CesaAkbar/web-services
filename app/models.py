import pymysql
from pymysql.cursors import DictCursor
import os


class Database:
    def koneksi(self):
        return pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT")),
            cursorclass=DictCursor
        )

class Services:
    def tampil_services(self):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        cursor.execute('''select customer.id, 
                            customer.no_spk, 
                            customer.nama, 
                            customer.alamat, 
                            customer.no_tlpn,
                            customer.tgl_spk, 
                            service_ac.id,
                            service_ac.tanggal_kunjungan, 
                            service_ac.tanggal_selesai, 
                            service_ac.remark_unit, 
                            teknisi.nama,
                            datediff(service_ac.tanggal_selesai+1, customer.tgl_spk) as waktu_service,
                            service_ac.status_pekerjaan, 
                            service_ac.keterangan_service
                            from customer left join service_ac on customer.id = service_ac.customer_id 
                            left join teknisi on service_ac.teknisi_id = teknisi.id ''')
        data = cursor.fetchall()
        return data

    def tambah_services(self, customer_id, teknisi_id, tanggal_kunjungan, tanggal_selesai, remak_unit):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        query = '''insert into service_ac 
                    (customer_id, 
                    teknisi_id, 
                    tanggal_kunjungan, 
                    tanggal_selesai, 
                    remark_unit) 
                    values (%s, %s, %s, %s, %s)'''
        cursor.execute(query,(customer_id, teknisi_id, tanggal_kunjungan, tanggal_selesai, remak_unit))
        koneksi.commit()
        cursor.close()
        koneksi.close()


    def ubah_services(self, teknisi_id, tanggal_kunjungan, tanggal_selesai, remak_unit, status_pekerjaa, keterangan_service,id):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        query = ('''update service_ac set 
                 teknisi_id= %s,
                 tanggal_kunjungan = %s,
                 tanggal_selesai = %s, 
                 remark_unit = %s,
                 status_pekerjaan = %s,
                 keterangan_service = %s 
                 where id = %s''')
        cursor.execute(query,(teknisi_id, tanggal_kunjungan, tanggal_selesai, remak_unit,status_pekerjaa, keterangan_service, id))
        koneksi.commit()
        cursor.close()
        koneksi.close()

    def form_tambah_services(self, id):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        cursor.execute('''select customer.id as customer_id,
                            customer.no_spk, 
                            customer.nama, 
                            teknisi.id as teknisi_id,
                            service_ac.remark_unit, 
                            service_ac.tanggal_kunjungan, 
                            service_ac.tanggal_selesai 
                            from customer left join service_ac on customer.id = service_ac.customer_id 
                            left join teknisi on service_ac.teknisi_id = teknisi.id where customer.id = %s''', (id,))
        data = cursor.fetchall()
        cursor.close()
        koneksi.close()
        print(data)
        return data

    def form_ubah_services(self, id):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        cursor.execute('''select service_ac.id, 
                    service_ac.customer_id ,
                    customer.nama,
                    service_ac.teknisi_id,
                    service_ac.tanggal_kunjungan,
                    service_ac.tanggal_selesai,
                    service_ac.remark_unit,
                    service_ac.status_pekerjaan,
                    service_ac.keterangan_service
                    from service_ac join customer on service_ac.customer_id = customer.id
                    where service_ac.id = %s''', (id,))
        data = cursor.fetchall()
        print(data)
        return data

    def hapus_services(self, id):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        query = "delete from service_ac where id = %s"
        cursor.execute(query, (id,))
        koneksi.commit()
        cursor.close()
        koneksi.close()

    def selisih_service(self):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor()
        cursor.execute('''select customer.id, 
                            customer.tgl_spk, 
                            service_ac.tanggal_selesai 
                            from customer join service_ac on customer.id = service_ac.customer_id''')
        data = cursor.fetchall()
        for row in data:
            service_id = row[0]
            tgl_spk = row[1]
            tgl_selesai = row[2]
            print(tgl_spk)
            print(tgl_selesai)
            waktu_service = (tgl_selesai - tgl_spk).days
            cursor.execute('update service_ac set selisih = %s where id = %s', (waktu_service, service_id))
        koneksi.commit()
        cursor.close()
        koneksi.close()

    def tampil_detail_services(self):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        cursor.execute("Select * from service_ac")
        data = cursor.fetchall()
        return data
#Customer
class Customers:
    def tampil_customers(self):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        cursor.execute("select * from customer")
        data = cursor.fetchall()
        cursor.close()
        koneksi.close()
        return data


    def tambah_customers(self, no_spk, nama, alamat, no_tlpn, sn_indoor, model_indoor, sn_outdoor, model_outdoor,
                          tgl_spk, kerusakan, garansi):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        query = 'insert into customer (no_spk ,nama, alamat, no_tlpn, sn_indoor, model_indoor, sn_outdoor, model_outdoor, tgl_spk, kerusakan, garansi) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (no_spk, nama, alamat, no_tlpn, sn_indoor, model_indoor, sn_outdoor,
                                  model_outdoor, tgl_spk, kerusakan, garansi))
        koneksi.commit()
        cursor.close()
        koneksi.close()

    def ubah_customers(self,
                       no_spk, nama, alamat, no_tlpn, sn_indoor, model_indoor,
                       sn_outdoor, model_outdoor, tgl_spk, kerusakan, garansi, id):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        query = ('''update customer set no_spk = %s,
                 nama = %s,
                 alamat = %s, 
                 no_tlpn = %s, 
                 sn_indoor = %s,
                 model_indoor = %s,
                 sn_outdoor = %s,
                 model_outdoor = %s,
                 tgl_spk = %s,
                 kerusakan = %s,
                 garansi = %s where id = %s''')
        cursor.execute(query, (no_spk, nama,alamat, no_tlpn, sn_indoor,
                               model_indoor, sn_outdoor,model_outdoor, tgl_spk, kerusakan, garansi, id))
        koneksi.commit()
        cursor.close()
        koneksi.close()

    def form_ubah_customer(self, id):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        cursor.execute("select * from customer where id = %s",(id,))
        data = cursor.fetchall()
        cursor.close()
        koneksi.close()
        return data

    def hapus_customer(self, id):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        query = "delete from customer where id = %s"
        cursor.execute(query, (id,))
        koneksi.commit()
        cursor.close()
        koneksi.close()

#Teknisi
class Teknisi:
    def tampil_teknisi(self):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        cursor.execute("select * from teknisi")
        data = cursor.fetchall()
        return data

    def ubah_teknisi(self,id, nama, no_tlpn):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        query = "update teknisi set nama = %s, no_tlpn = %s where id = %s"
        cursor.execute(query, (nama, no_tlpn, id))
        koneksi.commit()
        cursor.close()
        koneksi.close()


    def form_ubah_teknisi(self, id):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        cursor.execute("select * from teknisi where id = %s",(id,))
        data = cursor.fetchall()
        return data


    def tambah_teknisi(self, nama, no_tlpn):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        query = "INSERT INTO teknisi (nama, no_tlpn) VALUES (%s, %s)"
        cursor.execute(query, (nama, no_tlpn))
        koneksi.commit()
        cursor.close()
        koneksi.close()


    def hapus_teknisi(self, id):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        query = "delete from teknisi where id = %s"
        cursor.execute(query, (id,))
        koneksi.commit()
        cursor.close()
        koneksi.close()


#Data 3 Hari Service
class Complation:
    def tampil_data_complation(self, bulan):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        cursor.execute('''select customer.no_spk,
                            customer.nama,
                            customer.alamat,
                            customer.tgl_spk,
                            service_ac.tanggal_selesai,
                            service_ac.keterangan_service,
                            datediff(service_ac.tanggal_selesai, customer.tgl_spk) as waktu_service
                            from service_ac join customer on customer.id = service_ac.customer_id
                            where month(service_ac.tanggal_selesai) = %s and datediff(service_ac.tanggal_selesai, customer.tgl_spk) = 3''', (bulan,))
        data = cursor.fetchall()
        cursor.close()
        koneksi.close()
        return data

#Data 1 Hari Service
class Dispath:
    def tampil_data_dispath(self, bulan):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor(DictCursor)
        cursor.execute('''select customer.no_spk,
                                    customer.nama,
                                    customer.alamat,
                                    customer.tgl_spk,
                                    service_ac.tanggal_selesai,
                                    service_ac.keterangan_service,
                                    datediff(service_ac.tanggal_selesai, customer.tgl_spk) as waktu_service
                                    from service_ac join customer on customer.id = service_ac.customer_id
                                    where month(service_ac.tanggal_selesai) = %s 
                                    and datediff(service_ac.tanggal_selesai, customer.tgl_spk) between 1 and 2''',(bulan,))
        data = cursor.fetchall()
        cursor.close()
        koneksi.close()
        return data

#Login
class Login (object):
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def authenticate(self):
        koneksi = Database().koneksi()
        cursor = koneksi.cursor()
        cursor.execute("select count(*) from pengguna where username = %s and password = %s",(self.username, self.password) )
        n = (cursor.fetchone()) [0]
        cursor.close()
        koneksi.close()
        return True if n == 1 else False