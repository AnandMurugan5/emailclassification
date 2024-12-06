import os
import imaplib
import email
from email.header import decode_header

class EmailAttachmentDownloader:
    def __init__(self, username, password, server="imap.gmail.com", folder="inbox"):
        self.username = username
        self.password = password
        self.server = server
        self.folder = folder
        self.imap = None

    def connect(self):
        """Connects to the email server and logs in."""
        try:
            self.imap = imaplib.IMAP4_SSL(self.server)
            self.imap.login(self.username, self.password)
            print("Connected and logged in successfully.")
        except Exception as e:
            print(f"Failed to connect: {e}")

    def disconnect(self):
        """Closes the connection to the email server."""
        if self.imap:
            self.imap.close()
            self.imap.logout()
            print("Disconnected from the server.")

    def download_attachments(self, output_folder="email_attachments", search_criteria="ALL"):
        """
        Downloads all attachments from emails based on the search criteria.

        Args:
            output_folder (str): Folder to save attachments.
            search_criteria (str): Search filter for emails (e.g., "ALL", "UNSEEN").
        """
        try:
            os.makedirs(output_folder, exist_ok=True)
            self.imap.select(self.folder)

            # Search for emails
            status, messages = self.imap.search(None, search_criteria)
            if status != "OK":
                print("No emails found.")
                return

            email_ids = messages[0].split()
            for email_id in email_ids:
                # Fetch the email by ID
                res, msg = self.imap.fetch(email_id, "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        self._process_email(response[1], output_folder)
        except Exception as e:
            print(f"Error while downloading attachments: {e}")

    def _process_email(self, raw_email, output_folder):
        """Processes a single email and saves its attachments."""
        msg = email.message_from_bytes(raw_email)

        # Decode the email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        print(f"Processing email: {subject}")

        # If the email has attachments
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_disposition() == "attachment":
                    filename = part.get_filename()
                    if filename:
                        filename = self._decode_filename(filename)
                        filepath = os.path.join(output_folder, filename)
                        with open(filepath, "wb") as file:
                            file.write(part.get_payload(decode=True))
                        print(f"Downloaded: {filepath}")

    def _decode_filename(self, filename):
        """Decodes the filename from email headers."""
        decoded_name = decode_header(filename)[0][0]
        if isinstance(decoded_name, bytes):
            decoded_name = decoded_name.decode("utf-8")
        return decoded_name


# if __name__ == "__main__":
#     username = "muruganandham.r249@gmail.com"
#     password = "qgoa skfi oqja izug"

#     downloader = EmailAttachmentDownloader(username, password)
#     try:
#         downloader.connect()
#         downloader.download_attachments()
#     finally:
#         downloader.disconnect()
