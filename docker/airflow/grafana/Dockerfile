# optional: small Grafana image extension to copy dashboards/provisioning
FROM grafana/grafana:10.4.3
USER root
RUN mkdir -p /var/lib/grafana/dashboards
COPY provisioning /etc/grafana/provisioning
COPY dashboards /var/lib/grafana/dashboards
USER grafana
