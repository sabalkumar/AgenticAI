# Career Chat with AWS SES Notifications (SSO)

This version of the Career Chat application uses AWS SES (Simple Email Service) with AWS SSO authentication instead of Pushover for sending notifications.

## Setup Instructions

### 1. AWS Account Setup

1. **Create an AWS Account** (if you don't have one):
   - Visit https://aws.amazon.com/
   - Click "Create an AWS Account" and follow the signup process

2. **Set up AWS SSO**:
   - Go to AWS SSO Console: https://console.aws.amazon.com/singlesignon/
   - Follow the setup wizard to configure SSO for your account
   - Create a permission set with SES permissions (AmazonSESFullAccess)

3. **Configure AWS CLI with SSO**:
   ```bash
   aws configure sso
   ```
   - Enter your SSO start URL
   - Enter your SSO region
   - Enter your profile name (e.g., "career-chat")
   - Select your account and role

### 2. AWS SES Setup

1. **Go to SES Console**:
   - Visit https://console.aws.amazon.com/ses/
   - Make sure you're in the ap-southeast-2 region

2. **Verify Your Email Address**:
   - Click "Verified identities" → "Create identity"
   - Choose "Email address"
   - Enter your email address
   - Click "Create identity"
   - Check your email and click the verification link

3. **Verify Recipient Email** (if in sandbox mode):
   - If you're in sandbox mode, you'll also need to verify the email address where you want to receive notifications
   - Follow the same process as above for the recipient email

4. **Request Production Access** (optional):
   - If you want to send to any email address, request production access
   - Click "Account dashboard" → "Request production access"
   - Fill out the form explaining your use case

### 3. Environment Variables

Add these to your `.env` file:

```bash
AWS_PROFILE=your_sso_profile_name
AWS_REGION=ap-southeast-2
SES_FROM_EMAIL=your_verified_email@example.com
SES_TO_EMAIL=your_notification_email@example.com
OPENAI_API_KEY=your_openai_api_key
```

### 4. Install Dependencies

```bash
# Using uv (recommended)
uv add boto3 python-dotenv openai pypdf gradio

# Or using requirements file
uv pip install -r requirements_aws_ses.txt
```

### 5. Update Personal Information

1. Replace `me/linkedin.pdf` with your LinkedIn profile PDF
2. Update `me/summary.txt` with your personal summary
3. Update the `name` variable in the code with your name

### 6. Test the Setup

Run the notebook or the app:

```bash
# For the notebook
jupyter notebook 4_lab4_aws_ses.ipynb

# For the app
python app_aws_ses.py
```

### 7. Deploy to HuggingFace Spaces

**Note**: For deployment to HuggingFace Spaces, you'll need to use access keys instead of SSO since the deployment environment won't have access to your local SSO session.

1. Visit https://huggingface.co and create an account
2. Create a new Space
3. Upload your files
4. Add these secrets in the Space settings:
   - `AWS_ACCESS_KEY_ID` (temporary access key for deployment)
   - `AWS_SECRET_ACCESS_KEY` (temporary secret key for deployment)
   - `AWS_REGION` (ap-southeast-2)
   - `SES_FROM_EMAIL`
   - `SES_TO_EMAIL`
   - `OPENAI_API_KEY`

## Key Differences from Pushover Version

- **Notifications**: Instead of push notifications to your phone, you'll receive email notifications
- **Setup**: Requires AWS account and SES configuration instead of Pushover account
- **Authentication**: Uses AWS SSO for secure authentication instead of access keys
- **Cost**: AWS SES is very cost-effective (first 62,000 emails per month are free when sent from EC2)
- **Reliability**: AWS SES is highly reliable and scalable

## Troubleshooting

### Common Issues

1. **SSO session expired**: Run `aws sso login --profile your_profile_name` to refresh your session
2. **Email not verified**: Make sure both sender and recipient emails are verified in SES
3. **Sandbox mode**: In sandbox mode, you can only send to verified email addresses
4. **SSO permissions**: Ensure your SSO permission set includes SES permissions
5. **Region mismatch**: Make sure your AWS region matches in the code and console

### Error Messages

- `Email address not verified`: Add the email to verified identities in SES
- `MessageRejected`: Check if you're in sandbox mode and trying to send to unverified email
- `AccessDenied`: Check your SSO permission set includes SES permissions
- `ExpiredTokenException`: Your SSO session has expired, run `aws sso login`

### SSO Session Management

```bash
# Login to SSO
aws sso login --profile your_profile_name

# Check current session status
aws sts get-caller-identity --profile your_profile_name

# List available profiles
aws configure list-profiles
```

## Benefits of AWS SES with SSO

- **Cost-effective**: Very low cost per email
- **Scalable**: Can handle high volume
- **Reliable**: 99.9% uptime SLA
- **Secure**: Uses SSO for authentication instead of long-lived access keys
- **Integration**: Easy to integrate with other AWS services
- **Analytics**: Built-in delivery and bounce tracking 