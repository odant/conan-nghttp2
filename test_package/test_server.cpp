// Test for nghttp2 Conan package
// Dmitriy Vetutnev, Odant, 2018


#include <nghttp2/nghttp2ver.h>
#include <nghttp2/asio_http2_server.h>


#include <iostream>
#include <cstdlib>


using namespace nghttp2::asio_http2;
using namespace nghttp2::asio_http2::server;


int main(int, char**) {

    boost::system::error_code ec;
    boost::asio::ssl::context tls(boost::asio::ssl::context::sslv23);

    tls.use_private_key_file("selfsigned.key", boost::asio::ssl::context::pem);
    tls.use_certificate_chain_file("selfsigned.crt");

    configure_tls_context_easy(ec, tls);

    http2 server;

    server.handle("/index.html", [](const request &req, const response &res)
    {
        res.write_head(200);
        res.end(file_generator("index.html"));
    });

    const bool async = true;
    if ( server.listen_and_serve(ec, "localhost", "3000", async) ) {
        std::cerr << "Error: " << ec.message() << std::endl;
        std::exit(EXIT_FAILURE);
    }

    server.stop();
    server.join();

    return EXIT_SUCCESS;
}
