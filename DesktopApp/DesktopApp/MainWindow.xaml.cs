using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows;

namespace DesktopApp
{
    public partial class MainWindow : Window
    {
        private static readonly HttpClient httpClient = new HttpClient();
        public MainWindow()
        {
            InitializeComponent();
        }

        private async void SendButton_Click(object sender, RoutedEventArgs e)
        {
            string userInput = InputTextBox.Text.Trim();

            if (string.IsNullOrEmpty(userInput))
            {
                ResultTextBlock.Text = "❗ Пожалуйста, введите текст.";
                return;
            }

            try
            {
                // Блокировка кнопки во время запроса
                SendButton.IsEnabled = false;
                SendButton.Content = "Отправка...";

                ResultTextBlock.Text = "⏳ Ожидание ответа от сервера...";

                string jsonRequest = JsonSerializer.Serialize(new { text = userInput });
                var content = new StringContent(jsonRequest, Encoding.UTF8, "application/json");

                string apiUrl = "https://api.guvolution.com"; // замените на ваш реальный API

                HttpResponseMessage response = await httpClient.PostAsync(apiUrl, content);
                string jsonResponse = await response.Content.ReadAsStringAsync();

                if (!response.IsSuccessStatusCode)
                {
                    ResultTextBlock.Text = $"❌ Ошибка {(int)response.StatusCode}: {response.ReasonPhrase}\n{jsonResponse}";
                    return;
                }

                using JsonDocument doc = JsonDocument.Parse(jsonResponse);
                if (doc.RootElement.TryGetProperty("result", out JsonElement result))
                {
                    ResultTextBlock.Text = $"✅ Ответ:\n{result.GetString()}";
                }
                else
                {
                    ResultTextBlock.Text = "⚠️ Ответ не содержит поля 'result'.";
                }
            }
            catch (Exception ex)
            {
                ResultTextBlock.Text = $"🚫 Ошибка: {ex.Message}";
            }
            finally
            {
                SendButton.IsEnabled = true;
                SendButton.Content = "Отправить";
            }
        }
    }
}