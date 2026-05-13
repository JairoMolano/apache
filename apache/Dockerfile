FROM httpd:2.4

COPY miaplicacion.conf /usr/local/apache2/conf/extra/miaplication.conf

# Reemplazar la configuración principal de Apache para: Habilitar mod_proxy y mod_proxy_http, habilitar mod_headers e incluir el propio virtual host.
RUN echo "LoadModule proxy_module modules/mod_proxy.so" >> /usr/local/apache2/conf/httpd.conf && \
    echo "LoadModule proxy_http_module modules/mod_proxy_http.so" >> /usr/local/apache2/conf/httpd.conf && \
    echo "LoadModule headers_module modules/mod_headers.so" >> /usr/local/apache2/conf/httpd.conf && \
    echo "Include conf/extra/miaplication.conf" >> /usr/local/apache2/conf/httpd.conf

EXPOSE 80
