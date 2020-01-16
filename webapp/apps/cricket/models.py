from django.db import models
import jsonfield


class Country(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)


class Team(models.Model):    
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="team/logo/", max_length=700, blank=True, null=True)
    club_state = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to="player/profile/", max_length=700, blank=True, null=True)
    jersey_num = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.PROTECT, related_name = 'player_team')
    batting_history = jsonfield.JSONField()
    bowling_history = jsonfield.JSONField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class BattingHistory(models.Model):
    player = models.ForeignKey(Player, blank=True, null=True, on_delete=models.CASCADE)
    bt_match_played = models.IntegerField(default=0)
    ball_faced = models.IntegerField(default=0)
    bt_run = models.IntegerField(default=0)
    highest_score = models.IntegerField(default=0)
    fifties = models.IntegerField(default=0)
    hundreds = models.IntegerField(default=0)
    bt_strike_rate = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    bt_avgs = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)

    def __str__(self):
        return self.player.first_name + ' ' + self.player.last_name

class BowlingHistory(models.Model):
    player = models.ForeignKey(Player, blank=True, null=True, on_delete=models.CASCADE)
    bt_match_played = models.IntegerField(default=0)
    ball = models.IntegerField(default=0)
    bl_run = models.IntegerField(default=0)
    wicket = models.IntegerField(default=0)
    best_bowling = models.CharField(max_length=10, blank=True, null=True)
    economy = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    bl_strike_rate = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    bl_avgs = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)

    def __str__(self):
        return self.player.first_name + ' ' + self.player.last_name


class Series(models.Model):
    series_name = models.CharField(max_length=10, blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.series_name


class TeamsPerSeries(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name = 'serieswiseteams')
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name = 'teams_per_series')

    def __str__(self):
        return self.team.name + ' (' + self.series.series_name + ')'

class MatchesBetweenTeams(models.Model):
    series = models.ForeignKey(Series, blank=True, null=True, on_delete=models.CASCADE, related_name = 'series')
    date_of_match = models.DateField(null=True, blank=True)
    match_no = models.IntegerField(default=1)
    team1 = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE, related_name = 'team1')
    team2 = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE, related_name = 'team2')
    venue = models.CharField(max_length=100, blank=True, null=True)


class MatchResult(models.Model):
    series = models.ForeignKey(Series, blank=True, null=True, on_delete=models.CASCADE, related_name = 'result_series')
    match = models.ForeignKey(MatchesBetweenTeams, blank=True, null=True, on_delete=models.CASCADE, related_name='match')
    toss_winner = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE, related_name = 'toss_winner') 
    elected_to = models.CharField(max_length=10, blank=True, null=True)
    match_winner = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE, related_name='match_winner_team')
    man_of_the_match = models.ForeignKey(Player, blank=True, null=True, on_delete=models.CASCADE, related_name='match_performer')


class PointsTable(models.Model):
    series = models.ForeignKey(Series, blank=True, null=True, on_delete=models.CASCADE, related_name = 'pt_series')
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE, related_name='pt_team')
    match_played = models.IntegerField(default=0)
    match_won = models.IntegerField(default=0)
    match_lost = models.IntegerField(default=0)
    match_tied = models.IntegerField(default=0)
    no_result = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    net_runrate = models.DecimalField(decimal_places=3, max_digits=6, default=0.0)