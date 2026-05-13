# Imagen base oficial Apache (httpd)
FROM httpd:2.4

# Instalar el módulo proxy de Apache (viene en la imagen oficial
# pero necesita activarse copiando una httpd.conf personalizada)
# En lugar de eso, usamos la imagen con mod_proxy ya disponible
# y lo habilitamos vía script de entrada.

# Copiar nuestra configuración de virtual host
COPY miaplicacion.conf /usr/local/apache2/conf/extra/miaplicacion.conf

# Reemplazar la configuración principal de Apache para:
# 1. Habilitar mod_proxy y mod_proxy_http
# 2. Habilitar mod_headers
# 3. Incluir nuestro virtual host
RUN echo "LoadModule proxy_module modules/mod_proxy.so" >> /usr/local/apache2/conf/httpd.conf && \
    echo "LoadModule proxy_http_module modules/mod_proxy_http.so" >> /usr/local/apache2/conf/httpd.conf && \
    echo "LoadModule headers_module modules/mod_headers.so" >> /usr/local/apache2/conf/httpd.conf && \
    echo "Include conf/extra/miaplicacion.conf" >> /usr/local/apache2/conf/httpd.conf

EXPOSE 80
