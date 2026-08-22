from uuid import UUID

from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):
    def test_health_check_reports_api_available(self):
        response = self.client.get("/api/v1/health/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok", "service": "athena-api"})

    def test_response_has_correlation_identifier(self):
        response = self.client.get("/api/v1/health/")

        UUID(response["X-Request-ID"])

    def test_untrusted_correlation_identifier_is_replaced(self):
        response = self.client.get(
            "/api/v1/health/", headers={"X-Request-ID": "invalid\nlog-injection"}
        )

        self.assertNotEqual(response["X-Request-ID"], "invalid\nlog-injection")
        UUID(response["X-Request-ID"])
