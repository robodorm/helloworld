#
# Not tested (there is no AWS account available)
#

provider "aws" {}

data "archive_file" "lambda_helloapp" {
  type        = "zip"
  source_dir  = "${path.module}/.."
  output_path = "${path.module}/../helloapp.zip"
}

resource "aws_s3_bucket_object" "lambda_helloapp" {
  bucket = aws_s3_bucket.lambda_bucket.id
  key    = "helloapp.zip"
  source = data.archive_file.lambda_helloapp.output_path
  etag   = filemd5(data.archive_file.lambda_helloapp.output_path)
}

resource "aws_apigatewayv2_api" "lambda" {
  name          = "serverless_lambda_gw"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda" {
  api_id      = aws_apigatewayv2_api.lambda.id
  name        = "serverless_lambda_stage"
  auto_deploy = true
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn
    format          = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
    })
  }
}

resource "aws_apigatewayv2_integration" "helloapp" {
  api_id             = aws_apigatewayv2_api.lambda.id
  integration_uri    = aws_lambda_function.helloapp.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "helloapp" {
  api_id    = aws_apigatewayv2_api.lambda.id
  route_key = "GET /hello"
  target    = "integrations/${aws_apigatewayv2_integration.helloapp.id}"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name              = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"
  retention_in_days = 30
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.helloapp.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}
