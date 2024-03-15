
function openCity(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}



    document.addEventListener('DOMContentLoaded', function () {
        // Получение всех кнопок "Создать фильтр"
        var createFilterButtons = document.querySelectorAll('.create__filltre__modal');

        // Обработка нажатия на каждую кнопку
        createFilterButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                // Получение значения email из атрибута data-email
                var emailValue = button.getAttribute('data-email');

                // Использование регулярного выражения для извлечения адреса электронной почты из угловых скобок
                var emailMatch = emailValue.match(/<([^>]+)>/);

                // Проверка, был ли найден адрес электронной почты
                if (emailMatch) {
                    // Извлечение адреса из регулярного выражения
                    var cleanEmail = emailMatch[1];

                    // Установка очищенного значения в поле формы модального окна
                    document.getElementById('email').value = cleanEmail;
                } else {
                    console.log('Адрес электронной почты не найден.');
                }
            });
        });
    });