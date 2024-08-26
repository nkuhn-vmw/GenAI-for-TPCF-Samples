# Securing incoming traffic in Cloud Foundry
You can secure HTTP traffic into your Cloud Foundry deployment with TLS certificates. You can also configure the location
where your deployment stops TLS depending on your needs and certificate restrictions.

## Protocol support
The Gorouter supports HTTP/HTTPS requests only.
For more information about features supported by the Gorouter, see [HTTP Routing](https://docs.cloudfoundry.org/concepts/http-routing.html).
To secure non-HTTP traffic over TCP routing, terminate TLS at your load balancer or at the app. For more information, see [Enabling TCP Routing](https://docs.cloudfoundry.org/adminguide/enabling-tcp-routing.html).

## TLS termination options for HTTP routing
There are several options for terminating TLS for HTTP traffic. You can stop TLS at the Gorouter, your load balancer, or both.
The following table summarizes TLS termination options and which option to choose for your deployment:
| If the following applies to you: | Then configure TLS termination at: | Related topic and configuration procedure |
| --- | --- | --- |
| * You want the optimum balance of performance and security, and

* You want to make minimum changes to your load balancer, or

* You are deploying Cloud Foundry to AWS. For information about AWS limitations, see [TLS Cipher Suite Support by AWS ELBs](https://docs.cloudfoundry.org/adminguide/securing-traffic.html#aws_elbs).
| **Gorouter only** | [Terminating TLS at the Gorouter Only](https://docs.cloudfoundry.org/adminguide/securing-traffic.html#gorouter_term) |
| * You require TLS termination at a load balancer, or

* You want the highest level of security, and

* You do not mind a slightly less performant deployment.
| **Load Balancer and Gorouter** | [Terminating TLS at the Load Balancer and Gorouter](https://docs.cloudfoundry.org/adminguide/securing-traffic.html#lb_and_gorouter_term) |
| * You require TLS termination at a load balancer, and

* You prefer unencrypted traffic between the Load Balancer and the Gorouter.
| **Load Balancer only** | [Terminating TLS at the Load Balancer Only](https://docs.cloudfoundry.org/adminguide/securing-traffic.html#lb_term) |

## Certificate requirements
The following requirements apply to the certificates you use to secure traffic into Cloud Foundry:

* You must obtain at least one TLS certificate for your environment.

+ In a production environment, use a signed TLS certificate (trusted) from a known certificate authority (CA).

+ In a development or testing environment, you can use a trusted CA certificate or a self-signed certificate. You can generate a self-signed certificate with `openssl` or a similar tool.

* Certificates used in Cloud Foundry must be encoded in the PEM format.

* The Gorouter supports mutual TLS, and validates a client provided certificate chain against its CA certificates if one is provided in the TLS handshake, but does not require it. Depending on whether you choose to terminate at both the load balancer and the Gorouter, or at the Gorouter alone, the client certificate can be that of the load balancer or of the originating client.

* The certificate on the Gorouter must be associated with the correct host name so that HTTPS can validate the request.

* If wildcard certificates are not supported for some or all of your domains, then configure termination requests at the load balancer only. In this type of deployment, the load balancer passes unencrypted traffic to the Gorouter. As a result, you avoid having to reissue and reinstall certificates on the Gorouter for every app or UAA security zone.

* Extended Validation (EV) certificates support multiple host names, like SAN, but do not support wildcards. As the Gorouter has not been tested with EV certificates, if EV certificates are required, then terminate TLS at the load balancer only.

* Given the dynamic and multi-tenant nature of Cloud Foundry, Cloud Foundry highly recommends using wildcard domains to avoid the need for adding an additional certificate for each app.

* To support TLS v1.3, ensure that you use certificates generated with a key larger than 512 bits.

## Multiple certificates
In order to support custom domains on Cloud Foundry, an operator has to configure the Gorouter with a certificate that represents the domain. Cloud Foundry recommends that operators add a new certificate instead of reissuing a single certificate when adding TLS support for an additional domain. Using multiple certificates provides a security benefit in that it prevents clients from discovering all the custom domains of apps running on a Cloud Foundry platform.
The Gorouter supports SNI and can be configured with multiple certificates, each which can optionally have wildcard and alternative names. The Gorouter uses SNI to determine the correct certificate to present in a TLS handshake. It requires clients to support the SNI protocol by sending a server name outside the encrypted request payload. For clients that do not support SNI, the Gorouter presents a default certificate. The default is the first certificate keypair in the Gorouter’s configuration.
The Gorouter decides which certificate to provide in the TLS handshake as follows:

* If a client provides an SNI header with a ServerName that matches to a configured certificate keypair, the Gorouter returns the matching certificate.

* If a client provides an SNI header with a ServerName that does not match a configured certificate keypair, the Gorouter returns the default certificate.
The first certificate keypair listed is used as the default.
The Gorouter supports both RSA and ECDSA certificates in PEM encoding. In the case that a certificate chain is required, the order should be as follows: primary certificate, intermediate certificate, then root certificate.

### How to configure multiple certificate keypairs
To configure multiple HTTPS certificates for Cloud Foundry, specify those certificate keypairs in the `router.tls_pem` property.
The following is an example for configuring two certificate keypairs using `router.tls_pem`
```
properties:
router:
tls_pem:

- cert_chain: |

-----BEGIN CERTIFICATE-----
MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDg
MBQGCCqGSIb3DQMHBAgD1kGN4ZslJgSCBMi1xk9jhlPxPc
9g73NQbtqZwI+9X5OhpSg/2ALxlCCjbqvzgSu8gfFZ4yo+
A .... MANY LINES LIKE THAT ....
X0R+meOaudPTBxoSgCCM51poFgaqt4l6VlTN4FRpj+c/Wc
blK948UAda/bWVmZjXfY4Tztah0CuqlAldOQBzu8TwE7WD
H0ga/iLNvWYexG7FHLRiq5hTj0g9mUPEbeTXuPtOkTEb/0
GEs=

----END CERTIFICATE-----
private_key: |

-----BEGIN EXAMPLE ENCRYPTED PRIVATE KEY-----
MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDg
MBQGCCqGSIb3DQMHBAgD1kGN4ZslJgSCBMi1xk9jhlPxPc
9g73NQbtqZwI+9X5OhpSg/2ALxlCCjbqvzgSu8gfFZ4yo+
A .... MANY LINES LIKE THAT ....
X0R+meOaudPTBxoSgCCM51poFgaqt4l6VlTN4FRpj+c/Wc
blK948UAda/bWVmZjXfY4Tztah0CuqlAldOQBzu8TwE7WD
H0ga/iLNvWYexG7FHLRiq5hTj0g9mUPEbeTXuPtOkTEb/0
GEs=

-----END EXAMPLE ENCRYPTED PRIVATE KEY-----

- cert_chain: |

-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAJC1HiIAZAiIMA0GCSqGSIb3Df
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVx
aWRnaXRzIFB0eSBMdGQwHhcNMTExMjMxMDg1OTQ0WhcNMT
A .... MANY LINES LIKE THAT ....
JjyzfN746vaInA1KxYEeI1Rx5KXY8zIdj6a7hhphpj2E04
C3Fayua4DRHyZOLmlvQ6tIChY0ClXXuefbmVSDeUHwc8Yu
B7xxt8BVc69rLeHV15A0qyx77CLSj3tCx2IUXVqRs5mlSb
vA==

-----END CERTIFICATE-----
private_key: |

-----BEGIN EXAMPLE ENCRYPTED PRIVATE KEY-----
MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDg
MBQGCCqGSIb3DQMHBAgD1kGN4ZslJgSCBMi1xk9jhlPxPc
9g73NQbtqZwI+9X5OhpSg/2ALxlCCjbqvzgSu8gfFZ4yo+
A .... MANY LINES LIKE THAT ....
X0R+meOaudPTBxoSgCCM51poFgaqt4l6VlTN4FRpj+c/Wc
blK948UAda/bWVmZjXfY4Tztah0CuqlAldOQBzu8TwE7WD
H0ga/iLNvWYexG7FHLRiq5hTj0g9mUPEbeTXuPtOkTEb/0
GEs=

-----END EXAMPLE ENCRYPTED PRIVATE KEY-----
```

## TLS cipher suite support
Some Cloud Foundry components like the Gorouter support additional TLS cipher suites to accommodate older clients. As a security best practice, only configure the TLS cipher suites that you need for your deployment.

### Default Gorouter cipher suites
By default, the Gorouter supports the following TLS cipher suites:
| TLS Version | RFC | OpenSSL |
| --- | --- | --- |
| 1.2 | TLS\_ECDHE\_RSA\_WITH\_AES\_128\_GCM\_SHA256 | ECDHE-RSA-AES128-GCM-SHA256 |
| 1.2 | TLS\_ECDHE\_RSA\_WITH\_AES\_256\_GCM\_SHA384 | ECDHE-RSA-AES256-GCM-SHA384 |
| 1.3 | TLS\_AES\_128\_GCM\_SHA256 | TLS13-AES-128-GCM-SHA256 |
| 1.3 | TLS\_AES\_256\_GCM\_SHA384 | TLS13-AES-256-GCM-SHA384 |
| 1.3 | TLS\_CHACHA20\_POLY1305\_SHA256 | TLS13-CHACHA20-POLY1305-SHA256 |
You can override the default cipher suites by changing the `router.cipher_suites` and `router.min_tls_version` BOSH manifest properties.

### TLS cipher suite support by AWS load balancers
AWS Classic Load Balancers (formerly referred to as ELBs) support configuration of cipher suites for front end connections with clients only. When configuring Classic Load Balancers to forward requests to Gorouters over TLS, oyou might encounter a `Cipher Suite Mismatch` error. This is because the cipher suites supported by Classic Load Balancers for TLS handshakes with back ends (Gorouters in this case) are hardcoded, undocumented, and do not support the Gorouter default cipher suites.
You can configure TLS termination in one of the following ways:

* Configure Classic Load Balancer listeners in TCP mode. This allows TCP connections from clients to pass through the Classic Load Balancer to Gorouters on port 443. With this configuration, Gorouters are the first point of TLS termination.

* If you require TLS termination at an AWS load balancer in addition to terminating at the Gorouter, use [AWS Application Load Balancers (ALBs)](http://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) that support the Gorouter default cipher suites.

### TLS v1.3
You cannot configure cipher suites for TLS v1.3. Gorouter only supports the defaults listed in [Default Gorouter Cipher Suites](https://docs.cloudfoundry.org/adminguide/securing-traffic.html#default).
To support TLS v1.3, ensure the Gorouter is configured with certificates generated with a key larger than 512 bits.

### TLS v1.2
The following cipher suites are optionally supported for TLS v1.2 only:
| RFC | OpenSSL |
| --- | --- |
| TLS\_RSA\_WITH\_AES\_128\_GCM\_SHA256 | AES128-GCM-SHA256 |
| TLS\_RSA\_WITH\_AES\_256\_GCM\_SHA384 | AES256-GCM-SHA384 |
| TLS\_ECDHE\_ECDSA\_WITH\_RC4\_128\_SHA | ECDHE-ECDSA-RC4-SHA |
| TLS\_ECDHE\_ECDSA\_WITH\_AES\_128\_CBC\_SHA | ECDHE-ECDSA-AES128-SHA |
| TLS\_ECDHE\_ECDSA\_WITH\_AES\_256\_CBC\_SHA | ECDHE-ECDSA-AES256-SHA |
| TLS\_ECDHE\_RSA\_WITH\_RC4\_128\_SHA | ECDHE-RSA-RC4-SHA |
| TLS\_ECDHE\_RSA\_WITH\_3DES\_EDE\_CBC\_SHA | ECDHE-RSA-DES-CBC3-SHA |
| TLS\_ECDHE\_RSA\_WITH\_AES\_128\_CBC\_SHA | ECDHE-RSA-AES128-SHA |
| TLS\_ECDHE\_RSA\_WITH\_AES\_256\_CBC\_SHA | ECDHE-RSA-AES256-SHA |
| TLS\_ECDHE\_RSA\_WITH\_AES\_128\_GCM\_SHA256 | ECDHE-RSA-AES128-GCM-SHA256 |
| TLS\_ECDHE\_ECDSA\_WITH\_AES\_128\_GCM\_SHA256 | ECDHE-ECDSA-AES128-GCM-SHA256 |
| TLS\_ECDHE\_RSA\_WITH\_AES\_256\_GCM\_SHA384 | ECDHE-RSA-AES256-GCM-SHA384 |
| TLS\_ECDHE\_ECDSA\_WITH\_AES\_256\_GCM\_SHA384 | ECDHE-ECDSA-AES256-GCM-SHA384 |
| TLS\_RSA\_WITH\_AES\_128\_CBC\_SHA256 | AES128-SHA256 |
| TLS\_ECDHE\_ECDSA\_WITH\_AES\_128\_CBC\_SHA256 | ECDHE-ECDSA-AES128-SHA256 |
| TLS\_ECDHE\_RSA\_WITH\_AES\_128\_CBC\_SHA256 | ECDHE-RSA-AES128-SHA256 |
| TLS\_ECDHE\_RSA\_WITH\_CHACHA20\_POLY1305 | ECDHE-RSA-CHACHA20-POLY1305 |
| TLS\_ECDHE\_ECDSA\_WITH\_CHACHA20\_POLY1305 | ECDHE-ECDSA-CHACHA20-POLY1305 |

### TLS v1.0 and v1.1
The following cipher suites are optionally supported for TLS v1.0 and TLS v1.1 only:
| RFC | OpenSSL |
| --- | --- |
| TLS\_RSA\_WITH\_RC4\_128\_SHA | RC4-SHA |
| TLS\_RSA\_WITH\_3DES\_EDE\_CBC\_SHA | DES-CBC3-SHA |
| TLS\_RSA\_WITH\_AES\_128\_CBC\_SHA | AES128-SHA |
| TLS\_RSA\_WITH\_AES\_256\_CBC\_SHA | AES256-SHA |
You can override the default cipher suites by changing the `router.cipher_suites` and `router.min_tls_version` BOSH manifest properties.
For more information about supported ciphers, see [Golang Constants](https://github.com/golang/go/blob/release-branch.go1.7/src/crypto/tls/cipher_suites.go#L269-L285) in the Golang repository on GitHub and [Ciphers](https://www.openssl.org/docs/man1.1.1/man1/ciphers.html) in the OpenSSL documentation.

**Note**
ECDSA ciphers require a certificate and key for DSA, as opposed to RSA.

## Mutual authentication with clients
The Gorouter supports validation of client certificates in TLS handshakes with clients, also known as mutual authentication. Operators can choose whether the Gorouter requests client certificates and when requesting certificates, whether or not to require them.
By default, the Gorouter requests but does not require client certificates in TLS handshakes.

## Terminating TLS at the Gorouter only
In this configuration, the load balancer does not terminate TLS for Cloud Foundry domains at all. Instead, it passes through the underlying TCP connection to the Gorouter.
Cloud Foundry recommends this more performant option, establishing and terminating a single TLS connection.
The following diagram illustrates communication between the client, load balancer, Gorouter, and app.
![Diagram of the TLS Pass-Through.](https://docs.cloudfoundry.org/adminguide/images/pass-through.png)
The preceding diagram shows communication between the client, load balancer, router, and the app.
Traffic passes from the encrypted client, to the load balancer, to the router, and traffic ends at the app.
Traffic between the load balancer and the Gorouter is encrypted only if the client request is encrypted.
Traffic between the Gorouter and app is encrypted with TLS, unless a Windows stemcell is being used.

### About HTTP header forwarding
If you stop TLS at the Gorouter only, your load balancer does not send HTTP headers.
The Gorouter appends the `X-Forwarded-For` and `X-Forwarded-Proto` headers to requests forwarded to apps and platform system components.
`X-Forwarded-For` is set to the IP address of the source. Depending on the behavior of your load balancer, this can be the IP address of your load balancer. For the Gorouter to deliver the IP address of the client to apps, configure your load balancer to forward the IP address of the client or configure your load balancer to send the client IP address using the PROXY protocol.
`X-Forwarded-Proto` provides the scheme of the HTTP request from the client. The scheme is HTTP if the client made a request on port 80 (unencrypted) or HTTPS if the client made a request on port 443 (encrypted). The Gorouter sanitizes the `X-Forwarded-Proto` header based on the settings of the `router.sanitize_forwarded_proto` and `router.force_forwarded_proto_https` manifest properties as follows:

* `router.sanitize_forwarded_proto: true` and `router.force_forwarded_proto_https: true`: The Gorouter sets the value of `X-Forwarded-Proto` header to `HTTPS` in requests forwarded to back ends.

* `router.sanitize_forwarded_proto: true` and `router.force_forwarded_proto_https: false`: The Gorouter strips the `X-Forwarded-Proto` header when present in requests from front end clients. When the request is received on port 80 (unencrypted), the Gorouter sets the value of this header to `HTTP` in requests forwarded to back ends, When the request is received on port 443 (encrypted), the Gorouter sets the value of this header to `HTTPS`.

* `router.sanitize_forwarded_proto: false` and `router.force_forwarded_proto_https: true`: The Gorouter passes through the header as received from the load balancer, without modification.

* `router.sanitize_forwarded_proto: false` and `router.force_forwarded_proto_https: false`: The Gorouter passes through the header as received from the load balancer, without modification.
If you configured TLS to stop at the Gorouter only, Cloud Foundry recommends setting `router.sanitize_forwarded_proto: true` and `router.force_forwarded_proto_https: false` to secure against header spoofing.
For more information about HTTP headers in Cloud Foundry, see [HTTP Headers](https://docs.cloudfoundry.org/concepts/http-routing.html#http-headers) in *HTTP Routing*. For more information about configuring the forwarding of client certificates, see [Forward Client Certificate to Apps](https://docs.cloudfoundry.org/concepts/http-routing.html#forward-client-cert) in *HTTP Routing*.

### Procedure: Gorouter only
To enable this configuration, perform the following steps:

1. Configure your load balancer to pass through requests from the client to the Gorouter.

2. Insert the certificates into your deployment manifest for the Gorouter:

1. Open your release manifest with a text editor.

2. Copy the contents of your certificate chain and private key associated with your certificate into the `properties.router.tls_pem` field.

3. Set `enable_ssl` to `true`.
```
properties:
router:
tls_pem:

- cert_chain: |

-----BEGIN CERTIFICATE-----
SSL_CERTIFICATE_SIGNED_BY_PRIVATE_KEY

-----END CERTIFICATE-----
private_key: |

-----BEGIN EXAMPLE RSA PRIVATE KEY-----
RSA_PRIVATE_KEY

-----END EXAMPLE RSA PRIVATE KEY-----
enable_ssl: true
```

## Stopping TLS at the load balancer only
In this configuration, your load balancer terminates TLS and passes unencrypted traffic to the Gorouter, which routes it to your app. Traffic between the load balancer and the Gorouter is not encrypted.
Cloud Foundry recommends this option if you cannot use SAN certificates and if you do not require traffic to be encrypted between the load balancer and the Gorouter.
The following diagram illustrates communication between the client, load balancer, Gorouter, and app.
![Diagram of the TLS Termination at Load Balancer.](https://docs.cloudfoundry.org/adminguide/images/lb.png)
The preceding diagram shows configuration of the the client, load balancer, Gorouter, and app when the TLS terminates at the load balancer with lock icons.
Traffic starts at the encrypted client, passes through the load balancer to the router, and terminates at the app. Traffic is not encrypted past the load balancer.
Traffic between the Gorouter and app is encrypted with TLS, unless a Windows stemcell is being used.

### About HTTP header forwarding
If you stop TLS at your load balancer, you must also configure the load balancer to append the `X-Forwarded-For` and `X-Forwarded-Proto` HTTP headers to the HTTP traffic it passes to the Gorouter.
For more information about HTTP headers in Cloud Foundry, see [HTTP Headers](https://docs.cloudfoundry.org/concepts/http-routing.html#http-headers) in *HTTP Routing*. If you are configuring the forwarding of client certificates, see [Forward Client Certificate to Apps](https://docs.cloudfoundry.org/concepts/http-routing.html#forward-client-cert) in *HTTP Routing*.

### Procedure: Load balancer only
To enable this configuration, you must perform the following steps:

1. Add your certificates to your load balancer and configure the listening port. The procedures vary depending on your IaaS.

2. Configure your load balancer to append the `X-Forwarded-For` and `X-Forwarded-Proto` headers to client requests.

* If the load balancer cannot be configured to provide the `X-Forwarded-For` header, the Gorouter appends it in requests that are
forwarded to applications and system components, and sets the IP address of the load balancer.You must configure the load balancer to forward the `X-Forwarded-Proto` header. Otherwise requests to some
applications and system components result in redirect loops, as requests determined to be unencrypted are
redirected to HTTPS.

## Terminating TLS at the load balancer and Gorouter
In this configuration, two TLS connections are established: one from the client to the load balancer, and another from the load balancer to the Gorouter. This configuration secures all traffic between the load balancer and the Gorouter.
The following diagram illustrates communication between the client, load balancer, Gorouter, and app.
![TLS Termination at load balancer and router.](https://docs.cloudfoundry.org/adminguide/images/lb-and-router.png)
Traffic starts at the encrypted client, moves through the load balancer to the router, and terminates at the unencrypted app.
Traffic is encrypted between the client and load balancer, and between the load balancer and router.
This option is less performant, but allows for termination at a load balancer, as well as secure traffic between the load balancer and the Gorouter.
Traffic between the Gorouter and app is encrypted with TLS, unless a Windows stemcell is being used.

### Certificate guidelines
In this deployment scenario, the following guidelines apply:

* Certificates for the Cloud Foundry domains must be stored on the load balancer, as well as on the Gorouter.

* Generate certificates for your load balancer and the Gorouter with different keys. If the key for the certificate on the Gorouter is compromised, then the certificate on the load balancer is not at risk, and vice-versa.

* If you choose to host only one certificate on the Gorouter and many on your load balancer, configure your load balancer with the CA and host name with which to validate the certificate hosted by the Gorouter.

### About host name verification
Host name verification between the load balancer and the Gorouter is unnecessary when the load balancer is already configured with the Gorouter’s IP address to correctly route the request.
If the load balancer uses DNS resolution to route requests to the Gorouters, then you should enable host name verification.

### About HTTP header forwarding
If you terminate TLS at your load balancer, you must configure the load balancer to append the `X-Forwarded-For` and `X-Forwarded-Proto` HTTP headers to requests it sends to the Gorouter.
If you terminate TLS at your load balancer but it does not support HTTP, such that it cannot append HTTP headers, a workaround exists. You should use this workaround **only if your load balancer does not accept unencrypted requests**. Configure your load balancer to send the client IP address using the PROXY protocol, and enable PROXY in the Gorouter. As the `X-Forwarded-Proto` header is stripped, configure the Gorouter to force-set this header to ‘HTTPS’.
For more information about HTTP headers in Cloud Foundry, see [HTTP Headers](https://docs.cloudfoundry.org/concepts/http-routing.html#http-headers) in *HTTP Routing*. If you are configuring the forwarding of client certificates, see [Forward Client Certificate to Apps](https://docs.cloudfoundry.org/concepts/http-routing.html#forward-client-cert) in *HTTP Routing*.

### Procedure: Load balancer and Gorouter
To enable this configuration, use the following steps:

1. Add your certificates to your load balancer and configure the listening port. The procedures vary depending on your IaaS.

2. Configure your load balancer to append the `X-Forwarded-For` and `X-Forwarded-Proto` headers to client requests.
If the load balancer cannot be configured to provide the `X-Forwarded-For` header, the
Gorouter appends it in requests that are forwarded to applications and system components, and sets the IP address of the load balancer.
If the load balancer accepts unencrypted requests, it **must** provide the X-Forwarded-Proto header. Conversely, if the
load balancer cannot be configured to send the X-Forwarded-Proto header, it cannot not accept unencrypted requests.
Otherwise, applications and platform system components that depend on the X-Forwarded-Proto header to
reject unencrypted client requests and accept unencrypted requests.

3. Insert the certificates into your deployment manifest for the Gorouter:

1. Open your release manifest with a text editor.

2. Copy the contents of your certificate chain and private key that is associated with your certificate into the `properties.router.tls_pem` field.

3. Set `enable_ssl` to `true`.
```
properties:
router:
tls_pem:

- cert_chain: |

-----BEGIN CERTIFICATE-----
SSL_CERTIFICATE_SIGNED_BY_PRIVATE_KEY

-----END CERTIFICATE-----
private_key: |

-----BEGIN EXAMPLE RSA PRIVATE KEY-----
RSA_PRIVATE_KEY

-----END EXAMPLE RSA PRIVATE KEY-----
enable_ssl: true
```